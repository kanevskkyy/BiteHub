from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db

class ReviewStatus(db.Model):
    __tablename__ = 'review_statuses'

    id = db.Column(UUID, primary_key=True, default=uuid4)
    name = db.Column(db.String(20), nullable=False)