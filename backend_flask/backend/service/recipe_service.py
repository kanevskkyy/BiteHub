from typing import Optional
from uuid import UUID

from flask_sqlalchemy.session import Session
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader, db
from backend.models import Recipe, RecipeIngredient, RecipeStep, RecipeCategory
from backend.repositories.recipe_repository import RecipeRepository
from backend.schemas.recipes.recipe_detail_schema import recipe_detail_schema
from backend.schemas.recipes.recipe_list_schema import recipe_list_schema
from backend.schemas.recipes.recipes_stats import RecipeWithStats


class RecipeService:
    @inject
    def __init__(self, repository: RecipeRepository):
        self.__repository = repository

    def get_recipes(self, filters: dict) -> dict:
        page = filters.get('page', 1)
        per_page = filters.get('per_page', 24)
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


    def create(self, data: dict, image_file: Optional[FileStorage] = None):
        if not image_file:
            raise ValueError('Recipe must have an image!')

        image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

        recipe = Recipe(
            title=data['title'],
            description=data['description'],
            duration=data['duration'],
            servings_count=data.get('servings_count', 1),
            author_id='22222222-2222-2222-2222-222222222222',   #todo: тут парсити токен
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
        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise ValueError(f'Recipe not found with id: {recipe_id}')

        recipe.title = data.get('title', recipe.title)
        recipe.description = data.get('description', recipe.description)
        recipe.duration = data.get('duration', recipe.duration)
        recipe.servings_count = data.get('servings_count', recipe.servings_count)

        if image_file:
            if recipe.image_url:
                CloudinaryUploader.delete_file(recipe.image_url)
            recipe.image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

        existing_steps = {step.id: step for step in recipe.steps}
        new_steps_data = data.get('steps', [])
        new_steps_ids = set()

        with db.session.no_autoflush:
            for step_data in new_steps_data:
                step_id = step_data.get('id')
                if step_id and step_id in existing_steps:
                    step = existing_steps[step_id]
                    step.step_number = step_data['step_number']
                    step.description = step_data['description']
                    new_steps_ids.add(step_id)
                else:
                    new_step = RecipeStep(
                        step_number=step_data['step_number'],
                        description=step_data['description'],
                        recipe=recipe
                    )
                    recipe.steps.append(new_step)

            for step in list(recipe.steps):
                if step.id not in new_steps_ids and step.id in existing_steps:
                    db.session.delete(step)

        existing_ingredients = {ri.ingredient_id: ri for ri in recipe.recipe_ingredients}
        new_ingredient_ids = set(data.get('ingredients_ids', []))

        for ing_id in new_ingredient_ids - existing_ingredients.keys():
            recipe.recipe_ingredients.append(RecipeIngredient(ingredient_id=ing_id, recipe=recipe))

        for ing_id in existing_ingredients.keys() - new_ingredient_ids:
            db.session.delete(existing_ingredients[ing_id])

        existing_categories = {rc.category_id: rc for rc in recipe.recipe_categories}
        new_category_ids = set(data.get('category_ids', []))

        for cat_id in new_category_ids - existing_categories.keys():
            recipe.recipe_categories.append(RecipeCategory(category_id=cat_id, recipe=recipe))

        for cat_id in existing_categories.keys() - new_category_ids:
            db.session.delete(existing_categories[cat_id])

        updated_recipe = self.__repository.update(recipe)
        return recipe_detail_schema.dump(updated_recipe)

    from typing import Optional
    from uuid import UUID

    from flask_sqlalchemy.session import Session
    from injector import inject
    from werkzeug.datastructures import FileStorage

    from backend import CloudinaryUploader, db
    from backend.models import Recipe, RecipeIngredient, RecipeStep, RecipeCategory
    from backend.repositories.recipe_repository import RecipeRepository
    from backend.schemas.recipes.recipe_detail_schema import recipe_detail_schema
    from backend.schemas.recipes.recipe_list_schema import recipe_list_schema
    from backend.schemas.recipes.recipes_stats import RecipeWithStats

    class RecipeService:
        @inject
        def __init__(self, repository: RecipeRepository):
            self.__repository = repository

        def get_recipes(self, filters: dict) -> dict:
            page = filters.get('page', 1)
            per_page = filters.get('per_page', 24)
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

        def create(self, data: dict, image_file: Optional[FileStorage] = None):
            if not image_file:
                raise ValueError('Recipe must have an image!')

            image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

            recipe = Recipe(
                title=data['title'],
                description=data['description'],
                duration=data['duration'],
                servings_count=data.get('servings_count', 1),
                author_id='22222222-2222-2222-2222-222222222222',  # todo: тут парсити токен
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
            recipe = self.__repository.get_by_id(recipe_id)
            if not recipe:
                raise ValueError(f'Recipe not found with id: {recipe_id}')

            recipe.title = data.get('title', recipe.title)
            recipe.description = data.get('description', recipe.description)
            recipe.duration = data.get('duration', recipe.duration)
            recipe.servings_count = data.get('servings_count', recipe.servings_count)

            if image_file:
                if recipe.image_url:
                    CloudinaryUploader.delete_file(recipe.image_url)
                recipe.image_url = CloudinaryUploader.upload_file(image_file, folder='recipes')

            existing_steps = {step.id: step for step in recipe.steps}
            new_steps_data = data.get('steps', [])
            new_steps_ids = set()

            with db.session.no_autoflush:
                for step_data in new_steps_data:
                    step_id = step_data.get('id')
                    if step_id and step_id in existing_steps:
                        step = existing_steps[step_id]
                        step.step_number = step_data['step_number']
                        step.description = step_data['description']
                        new_steps_ids.add(step_id)
                    else:
                        new_step = RecipeStep(
                            step_number=step_data['step_number'],
                            description=step_data['description'],
                            recipe=recipe
                        )
                        recipe.steps.append(new_step)

                for step in list(recipe.steps):
                    if step.id not in new_steps_ids and step.id in existing_steps:
                        db.session.delete(step)

            existing_ingredients = {ri.ingredient_id: ri for ri in recipe.recipe_ingredients}
            new_ingredient_ids = set(data.get('ingredients_ids', []))

            for ing_id in new_ingredient_ids - existing_ingredients.keys():
                recipe.recipe_ingredients.append(RecipeIngredient(ingredient_id=ing_id, recipe=recipe))

            for ing_id in existing_ingredients.keys() - new_ingredient_ids:
                db.session.delete(existing_ingredients[ing_id])

            existing_categories = {rc.category_id: rc for rc in recipe.recipe_categories}
            new_category_ids = set(data.get('category_ids', []))

            for cat_id in new_category_ids - existing_categories.keys():
                recipe.recipe_categories.append(RecipeCategory(category_id=cat_id, recipe=recipe))

            for cat_id in existing_categories.keys() - new_category_ids:
                db.session.delete(existing_categories[cat_id])

            updated_recipe = self.__repository.update(recipe)
            return recipe_detail_schema.dump(updated_recipe)


    def delete(self, recipe_id: UUID) -> bool:
        recipe = self.__repository.get_by_id(recipe_id)
        if not recipe:
            raise ValueError(f'Recipe not found with id: {recipe_id}')

        if recipe.image_url:
            CloudinaryUploader.delete_file(recipe.image_url)

        self.__repository.delete(recipe)

        return True