from uuid import UUID

from backend import db
from backend.models import Reviews
from backend.pagination.paginated_result import PaginatedResult
from backend.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[Reviews]):
    def __init__(self):
        super().__init__(db.session, Reviews)

    def is_user_already_rated(self, user_id: UUID, recipe_id: UUID) -> bool:
        return (
                self._session.query(self._model)
                .filter(self._model.user_id == user_id, self._model.recipe_id == recipe_id)
                .first() is not None
        )

    def get_reviews_by_recipe(self, recipe_id: UUID, page: int = 1, per_page: int = 10) -> PaginatedResult:
        query = (
            self._session.query(self._model)
            .filter(self._model.recipe_id == recipe_id)
            .order_by(self._model.created_at.desc())
        )

        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            per_page=per_page
        )