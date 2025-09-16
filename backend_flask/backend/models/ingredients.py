from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import URLType

from backend.extensions import db


class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon_url = db.Column(URLType, nullable=False)

    recipe_ingredients = db.relationship(
        'RecipeIngredient',
        back_populates='ingredient',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    __table_args__ = (
        db.CheckConstraint('length(trim(name)) > 0', name='ck_ingredients_name_required'),
    )