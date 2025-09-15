from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import URLType

from backend.extensions import db


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    image_url = db.Column(URLType, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    servings_count = db.Column(db.Integer, nullable=False, default=1)

    author_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref='recipes')

    steps = db.relationship(
        'RecipeStep',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    recipe_ingredients = db.relationship(
        'RecipeIngredient',
        cascade='all, delete-orphan',
        passive_deletes=True
    )
    recipe_categories = db.relationship(
        'RecipeCategory',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    __table_args__ = (
        db.CheckConstraint('length(trim(title)) > 0', name='ck_recipes_title_required'),
        db.CheckConstraint('length(trim(description)) > 0', name='ck_recipes_description_required'),
        db.UniqueConstraint('author_id', 'title', name='uq_recipes_author_id_title'),
        db.CheckConstraint('duration > 0', name='ck_recipes_duration_valid'),
        db.CheckConstraint('servings_count > 0', name='ck_recipes_servings_count_valid'),
    )