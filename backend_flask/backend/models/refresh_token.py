from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db


class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    token = db.Column(db.String(255), nullable=False, unique=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='refresh_tokens')