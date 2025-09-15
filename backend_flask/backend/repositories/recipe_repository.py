from typing import Optional, List
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from backend import db
from backend.models import Recipe, Reviews, RecipeCategory, RecipeIngredient
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
        ingredient_ids: Optional[List[UUID]] = None
    ):
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

        query = query.group_by(Recipe.id).order_by(Recipe.created_at.desc())

        total = query.count()

        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            per_page=per_page
        )