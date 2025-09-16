from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from backend.extensions import db


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(80), nullable=False)