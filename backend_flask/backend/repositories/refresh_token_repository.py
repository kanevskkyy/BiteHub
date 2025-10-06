from typing import Optional
from uuid import UUID

from backend import db
from backend.models import RefreshToken
from backend.repositories.base_repository import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self):
        super().__init__(db.session, RefreshToken)

    def get_by_token(self, refresh_token: str) -> Optional[RefreshToken]:
        return self._session.query(self._model).filter_by(token=refresh_token).first()

    def delete_by_user_id(self, user_id: UUID) -> None:
        refresh_token = self._session.query(self._model).filter_by(user_id=user_id).first()
        if refresh_token:
            self._session.delete(refresh_token)