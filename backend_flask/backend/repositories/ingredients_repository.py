from uuid import UUID

from backend import db
from backend.models import Ingredients
from backend.repositories.base_repository import BaseRepository


class IngredientsRepository(BaseRepository[Ingredients]):
    def __init__(self):
        super().__init__(db.session, Ingredients)

    def is_name_exists(self, new_name: str, exclude_id: UUID = None) -> bool:
        query = self._session.query(self._model).filter(self._model.name == new_name)

        if exclude_id:
            query = query.filter(self._model.id != exclude_id)

        return query.first() is not None