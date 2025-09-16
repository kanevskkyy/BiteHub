from typing import Optional
from uuid import UUID

from flask_jwt_extended import get_jwt_identity, get_jwt
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader, db
from backend.models import Recipe, RecipeStep, RecipeIngredient, RecipeCategory
from backend.repositories.recipe_repository import RecipeRepository
from backend.schemas.recipes.recipe_detail_schema import recipe_detail_schema
from backend.schemas.recipes.recipe_list_schema import recipe_list_schema
from backend.schemas.recipes.recipes_stats import RecipeWithStats


class RecipeService:
    @inject
    def __init__(self, repository: RecipeRepository):
        self.__repository = repository


    def get_recipes(self, filters: dict) -> dict:
        page = int(filters.get('page', 1))
        per_page = int(filters.get('per_page', 24))
        user_id = filters.get('user_id')
        category_ids = filters.get('category_ids', [])
        ingredient_ids = filters.get('ingredient_ids', [])

        paginated = self.__repository.get_recipes_paginated(
            page=page,
            per_page=per_page,
            user_id=user_id,
            category_ids=category_ids,
            ingredient_ids=ingredient_ids
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

    def get_recipe_by_id(self, recipe_id: UUID) -> Optional[Recipe]:
        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise ValueError(f'Recipe not found with id: {recipe_id}')

        return recipe_detail_schema.dump(recipe)

    def create(self, data: dict, image_file: Optional[FileStorage]):
        user_id = get_jwt_identity()
        image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

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

    def update(self, recipe_id: UUID, data: dict, image_file: Optional[FileStorage] = None):
        user_id = get_jwt_identity()

        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise ValueError(f'Recipe not found with id: {recipe_id}')

        if recipe.author_id != user_id:
            raise ValueError(f'You don`\t have permission to edit this recipe')

        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.duration = data.get('duration', recipe.duration)
        recipe.servings_count = data.get('servings_count', recipe.servings_count)

        if image_file:
            if recipe.image_url:
                CloudinaryUploader.delete_file(recipe.image_url)
            recipe.image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

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
            raise ValueError(f'Recipe not found with id: {recipe_id}')

        if recipe.author_id != user_id and user_role != 'Admin':
            raise ValueError(f'You don`t have permission to delete this recipe')

        if recipe.image_url:
            CloudinaryUploader.delete_file(recipe.image_url)

        self.__repository.delete(recipe)

        return True