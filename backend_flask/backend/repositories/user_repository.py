from typing import Optional, Dict, Any
from uuid import UUID

from backend import db
from backend.models import User
from backend.pagination.paginated_result import PaginatedResult
from backend.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(db.session, User)

    def is_username_exist(self, username: str, exclude_id: UUID = None) -> bool:
        query = self._session.query(self._model).filter(
            self._model.username == username
        )
        if exclude_id:
            query = query.filter(self._model.id != exclude_id)

        return query.first() is not None