from typing import Optional
from uuid import UUID

from flask_jwt_extended import get_jwt_identity, get_jwt
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.exceptions import NotFound, PermissionDenied
from backend.models import Recipe, RecipeStep, RecipeIngredient, RecipeCategory
from backend.repositories import RecipeRepository, ReviewRepository
from backend.schemas import recipe_list_schema
from backend.schemas.recipes.recipe_detail_schema import recipe_detail_schema
from backend.schemas.recipes.recipes_stats import RecipeWithStats


class RecipeService:
    """
    Service for managing recipes, including CRUD operations, handling
    image uploads via Cloudinary, and providing user-specific flags
    like isReviewed or isApprovedReview.

    Methods:
        get_recipes(filters: dict) -> dict:
            Get paginated recipes with optional filters (user, categories, ingredients).

        get_recipe_by_id(recipe_id: UUID) -> dict:
            Get detailed info for a single recipe, including review flags for the current user.

        create(data: dict, image_file: Optional[FileStorage]):
            Create a new recipe with steps, ingredients, categories, and an optional image.

        update(recipe_id: UUID, data: dict, image_file: Optional[FileStorage]):
            Update a recipe, including steps, ingredients, categories, and optionally its image.
            Only the author can update their recipe.

        delete(recipe_id: UUID) -> bool:
            Delete a recipe. Only the author or Admin can delete.
    """
    @inject
    def __init__(self, repository: RecipeRepository, review_repo: ReviewRepository, cloud_uploader: CloudinaryUploader):
        self.__repository = repository
        self.__review_repo = review_repo
        self.__cloud_uploader = cloud_uploader


    def get_recipes(self, filters: dict) -> dict:
        page = int(filters.get('page', 1))
        per_page = int(filters.get('per_page', 24))
        user_id = filters.get('user_id')
        category_ids = filters.get('category_ids', [])
        ingredient_ids = filters.get('ingredient_ids', [])
        mode = filters.get('mode', 'or')

        paginated = self.__repository.get_recipes_paginated(
            page=page,
            per_page=per_page,
            user_id=user_id,
            category_ids=category_ids,
            ingredient_ids=ingredient_ids,
            mode = mode
        )

        recipes_with_stats = [
            RecipeWithStats(
                recipe=recipe,
                review_count=review_count,
                average_rating=float(average_rating) if average_rating else 0.0
            )
            for recipe, review_count, average_rating in paginated.items
        ]

        serialized_recipes = recipe_list_schema.dump(recipes_with_stats)

        return paginated.to_dict() | {'items': serialized_recipes}

    def get_recipe_by_id(self, recipe_id: UUID) -> Optional[dict]:
        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise NotFound(f'Recipe not found with id: {recipe_id}')

        serialized = recipe_detail_schema.dump(recipe)

        try:
            user_id = UUID(get_jwt_identity())
        except Exception:
            user_id = None

        if user_id:
            serialized['isReviewed'] = self.__review_repo.has_any_review(user_id, recipe_id)
            serialized['isApprovedReview'] = self.__review_repo.has_approved_review(user_id, recipe_id)
        else:
            serialized['isReviewed'] = False
            serialized['isApprovedReview'] = False

        return serialized

    def create(self, data: dict, image_file: Optional[FileStorage]) -> dict:
        user_id = get_jwt_identity()
        image_url = self.__cloud_uploader.upload_file(image_file, folder='recipes')

        recipe = Recipe(
            title=data['title'],
            description=data['description'],
            duration=data['duration'],
            servings_count=data.get('servings_count', 1),
            author_id=user_id,
            image_url=image_url,
        )

        for step in data.get('steps', []):
            recipe.steps.append(
                RecipeStep(
                    step_number=step['step_number'],
                    description=step['description'],
                )
            )

        for ingredient_id in data.get('ingredients_ids', []):
            recipe.recipe_ingredients.append(
                RecipeIngredient(ingredient_id=ingredient_id)
            )

        for category_id in data.get('category_ids', []):
            recipe.recipe_categories.append(
                RecipeCategory(category_id=category_id)
            )

        created_recipe = self.__repository.create(recipe)
        return recipe_detail_schema.dump(created_recipe)

    def update(self, recipe_id: UUID, data: dict, image_file: Optional[FileStorage] = None) -> dict:
        user_id = get_jwt_identity()

        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise NotFound(f'Recipe not found with id: {recipe_id}')

        if recipe.author_id != user_id:
            raise PermissionDenied(f'You don`\t have permission to edit this recipe')

        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.duration = data.get('duration', recipe.duration)
        recipe.servings_count = data.get('servings_count', recipe.servings_count)

        if image_file:
            if recipe.image_url:
                self.__cloud_uploader.delete_file(recipe.image_url)
            recipe.image_url = self.__cloud_uploader.upload_file(image_file, folder='recipes')

        self.__repository.update_steps(recipe, data.get('steps', []))
        self.__repository.update_ingredients(recipe, data.get('ingredients_ids', []))
        self.__repository.update_categories(recipe, data.get('category_ids', []))

        updated_recipe = self.__repository.update(recipe)
        return recipe_detail_schema.dump(updated_recipe)


    def delete(self, recipe_id: UUID) -> bool:
        user_id = get_jwt_identity()
        claims = get_jwt()
        user_role = claims.get('role')

        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise NotFound(f'Recipe not found with id: {recipe_id}')

        if recipe.author_id != user_id and user_role != 'Admin':
            raise PermissionDenied(f'You don`t have permission to delete this recipe')

        if recipe.image_url:
            self.__cloud_uploader.delete_file(recipe.image_url)

        self.__repository.delete(recipe)

        return True