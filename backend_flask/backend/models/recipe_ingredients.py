from sqlalchemy.dialects.postgresql import UUID
from backend.extensions import db


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id'), primary_key=True)
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'), primary_key=True)
    quantity = db.Column(db.String(40), nullable=False)

    recipe = db.relationship('Recipe', backref=db.backref('recipe_ingredients', lazy=True), foreign_keys=[recipe_id])
    ingredient = db.relationship('Ingredients', backref=db.backref('recipe_ingredients', lazy=True), foreign_keys=[ingredient_id])