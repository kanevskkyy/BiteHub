from marshmallow import Schema, fields, validates, ValidationError
from backend.schemas.recipes.recipe_step_schema import RecipeStepSchema


class RecipeCreateSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    duration = fields.Integer(required=True)
    servings_count = fields.Integer(required=True, data_key='servingsCount')
    steps = fields.List(fields.Nested(RecipeStepSchema), required=True)
    categoryIds = fields.List(fields.UUID(), required=True)
    ingredientsIds = fields.List(fields.UUID(), required=True)

    @validates('title')
    def validate_title(self, title: str, **kwargs) -> str:
        if title.strip() == '':
            raise ValidationError('Title cannot be empty')
        if len(title.strip()) > 100 or len(title.strip()) < 1:
            raise ValidationError('Title cannot be less than 100 characters')

        return title

    @validates('description')
    def validate_description(self, description: str, **kwargs) -> str:
        if description.strip() == '':
            raise ValidationError('Description cannot be empty')

        return description

    @validates('duration')
    def validate_duration(self, duration: int, **kwargs) -> int:
        if duration <= 0:
            raise ValidationError('Duration cannot be negative or zero')

        return duration

    @validates('servings_count')
    def validate_servings_count(self, servings_count: int, **kwargs) -> int:
        if servings_count <= 0:
            raise ValidationError('Servings count cannot be negative or zero')
        return servings_count


recipe_create_schema = RecipeCreateSchema()