from backend import db
from backend.models import Role
from backend.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(db.session, Role)

    def get_role_by_name(self, name: str) -> Role:
        return self._session.query(self._model).filter_by(name=name).first()