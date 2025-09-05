from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db


class RecipeCategory(db.Model):
    __tablename__ = 'recipe_categories'

    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id'), primary_key=True)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'), primary_key=True)

    recipe = db.relationship('Recipe', backref=db.backref('recipe_categories', lazy=True), foreign_keys=[recipe_id])
    category = db.relationship('Category', backref=db.backref('recipe_categories', lazy=True), foreign_keys=[category_id])
