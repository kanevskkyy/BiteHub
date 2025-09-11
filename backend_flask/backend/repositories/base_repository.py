from abc import ABC
from typing import TypeVar, Generic, List, Optional, Type

from flask_sqlalchemy.session import Session

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    def __init__(self, session: Session, model: Type[T]) -> None:
        self._session = session
        self._model = model

    def get_all(self) -> List[T]:
        return self._session.query(self._model).all()

    def get_by_id(self, id) -> Optional[T]:
        return self._session.get(self._model, id)

    def create(self, entity: T) -> T:
        self._session.add(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def update(self, entity: T) -> T:
        entity = self._session.merge(entity)
        self._session.commit()
        self._session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self._session.delete(entity)
        self._session.commit()