from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from backend.extensions import db


class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)
    calories = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.CheckConstraint('calories >= 0', name='ck_ingredients_calories_valid'),
        db.CheckConstraint('length(trim(name)) > 0', name='ck_ingredients_name_required'),
    )