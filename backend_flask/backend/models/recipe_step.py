from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from backend.extensions import db


class RecipeStep(db.Model):
    __tablename__ = 'recipe_steps'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    recipe_id = db.Column(UUID(as_uuid=True), db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    recipe = db.relationship('Recipe', backref='steps', lazy=True)

    __table_args__ = (
        db.CheckConstraint('step_number >= 1', name='ck_recipe_steps_step_number_valid'),
        db.CheckConstraint('length(trim(description)) > 0', name='ck_recipe_steps_description_required'),
    )