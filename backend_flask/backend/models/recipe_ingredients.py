from sqlalchemy.dialects.postgresql import UUID
from backend.extensions import db


class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id', ondelete='CASCADE'), primary_key=True)
    ingredient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ingredients.id'), primary_key=True)

    recipe = db.relationship('Recipe', back_populates='recipe_ingredients', overlaps='recipe_ingredients')
    ingredient = db.relationship('Ingredient', back_populates='recipe_ingredients', overlaps='recipe_ingredients')