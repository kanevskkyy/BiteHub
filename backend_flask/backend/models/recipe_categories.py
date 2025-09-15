from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db


class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'

    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'), primary_key=True)

    recipe = db.relationship('Recipe')
    category = db.relationship('Category')
