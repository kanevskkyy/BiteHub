from typing import Optional, List
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from backend import db
from backend.models import Recipe, Reviews, RecipeCategory, RecipeIngredient, RecipeStep
from backend.pagination.paginated_result import PaginatedResult
from backend.repositories.base_repository import BaseRepository


class RecipeRepository(BaseRepository[Recipe]):
    def __init__(self):
        super().__init__(db.session, Recipe)

    def is_recipe_title_for_user_exists(self, title: str, user_id: UUID) -> bool:
        return (
                self._session.query(self._model)
                .filter(self._model.title == title, self._model.author_id == user_id)
                .first() is not None
        )

    def get_recipes_paginated(
            self,
            page: int = 1,
            per_page: int = 24,
            user_id: Optional[UUID] = None,
            category_ids: Optional[List[UUID]] = None,
            ingredient_ids: Optional[List[UUID]] = None,
            mode: str = 'or'
    ) -> PaginatedResult:
        query = (
            self._session.query(
                Recipe,
                func.count(Reviews.id).label('review_count'),
                func.coalesce(func.avg(Reviews.rating), 0).label('average_rating')
            )
            .outerjoin(Reviews, Reviews.recipe_id == Recipe.id)
            .options(
                joinedload(Recipe.recipe_categories).joinedload(RecipeCategory.category),
                joinedload(Recipe.recipe_ingredients).joinedload(RecipeIngredient.ingredient),
            )
        )

        if user_id:
            query = query.filter(Recipe.author_id == user_id)

        if category_ids:
            query = query.join(RecipeCategory).filter(
                RecipeCategory.category_id.in_(category_ids)
            )

        if ingredient_ids:
            query = query.join(RecipeIngredient).filter(
                RecipeIngredient.ingredient_id.in_(ingredient_ids)
            )

            if mode == 'and':
                query = query.group_by(Recipe.id).having(
                    func.count(func.distinct(RecipeIngredient.ingredient_id)) == len(ingredient_ids)
                )

        query = query.group_by(Recipe.id).order_by(Recipe.created_at.desc())

        total = query.count()

        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            per_page=per_page
        )

    def update_steps(self, recipe, new_steps_data: list[dict]) -> None:
        existing_steps = {step.id: step for step in recipe.steps}
        new_steps_ids = set()

        with self._session.no_autoflush:
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
                    self._session.delete(step)

    def update_ingredients(self, recipe, new_ingredient_ids: List[UUID]) -> None:
        existing_ingredients = {ri.ingredient_id: ri for ri in recipe.recipe_ingredients}
        new_ids_set = set(new_ingredient_ids)

        for ing_id in new_ids_set - existing_ingredients.keys():
            recipe.recipe_ingredients.append(RecipeIngredient(ingredient_id=ing_id, recipe=recipe))

        for ing_id in existing_ingredients.keys() - new_ids_set:
            db.session.delete(existing_ingredients[ing_id])

    def update_categories(self, recipe, new_category_ids: List[UUID]) -> None:
        existing_categories = {rc.category_id: rc for rc in recipe.recipe_categories}
        new_ids_set = set(new_category_ids)

        for cat_id in new_ids_set - existing_categories.keys():
            recipe.recipe_categories.append(RecipeCategory(category_id=cat_id, recipe=recipe))

        for cat_id in existing_categories.keys() - new_ids_set:
            db.session.delete(existing_categories[cat_id])