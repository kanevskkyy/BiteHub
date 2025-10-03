from uuid import UUID

from backend import db
from backend.models import Ingredient
from backend.repositories.base_repository import BaseRepository


class IngredientRepository(BaseRepository[Ingredient]):
    def __init__(self):
        super().__init__(db.session, Ingredient)

    def is_name_exists(self, new_name: str, exclude_id: UUID = None) -> bool:
        query = self._session.query(self._model).filter(self._model.name == new_name)

        if exclude_id:
            query = query.filter(self._model.id != exclude_id)

        return query.first() is not None