from uuid import UUID
from backend import db
from backend.models import Reviews, ReviewStatus
from backend.pagination.paginated_result import PaginatedResult
from backend.repositories.base_repository import BaseRepository


class ReviewRepository(BaseRepository[Reviews]):
    def __init__(self):
        super().__init__(db.session, Reviews)

    def is_user_already_rated(self, user_id: UUID, recipe_id: UUID) -> bool:
        return (
                self._session.query(self._model)
                .filter(
                    self._model.user_id == user_id,
                    self._model.recipe_id == recipe_id,
                )
                .first() is not None
        )

    def has_any_review(self, user_id: UUID, recipe_id: UUID) -> bool:
        review = (
            self._session.query(self._model)
            .filter(
                self._model.user_id == user_id,
                self._model.recipe_id == recipe_id,
            )
            .first()
        )
        return review is not None

    def has_approved_review(self, user_id: UUID, recipe_id: UUID) -> bool:
        return (
                self._session.query(self._model)
                .join(ReviewStatus, ReviewStatus.id == self._model.status_id)
                .filter(
                    self._model.user_id == user_id,
                    self._model.recipe_id == recipe_id,
                    db.func.lower(ReviewStatus.name) == 'approved'
                )
                .first() is not None
        )

    def get_reviews_by_recipe(self, recipe_id: UUID, page: int = 1, per_page: int = 10) -> PaginatedResult:
        approved_status = (
            self._session.query(ReviewStatus)
            .filter(db.func.lower(ReviewStatus.name) == 'approved')
            .first()
        )

        if not approved_status:
            return PaginatedResult(items=[], total=0, page=page, per_page=per_page)

        query = (
            self._session.query(self._model)
            .filter(
                self._model.recipe_id == recipe_id,
                self._model.status_id == approved_status.id,
            )
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

    def get_pending_reviews(self, page: int = 1, per_page: int = 10) -> PaginatedResult:
        pending_status = (
            self._session.query(ReviewStatus)
            .filter(db.func.lower(ReviewStatus.name) == 'pending')
            .first()
        )

        if not pending_status:
            return PaginatedResult(items=[], total=0, page=page, per_page=per_page)

        query = (
            self._session.query(self._model)
            .filter(self._model.status_id == pending_status.id)
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

    def get_pending_status_id(self) -> UUID | None:
        pending_status = (
            self._session.query(ReviewStatus)
            .filter(db.func.lower(ReviewStatus.name) == 'pending')
            .first()
        )
        if pending_status:
            return pending_status.id

        return None

    def get_approve_status_id(self) -> UUID | None:
        pending_status = (
            self._session.query(ReviewStatus)
            .filter(db.func.lower(ReviewStatus.name) == 'approved')
            .first()
        )
        if pending_status:
            return pending_status.id

        return None