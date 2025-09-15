from marshmallow import Schema, fields, validate
from backend.schemas.recipes.recipe_step_schema import RecipeStepSchema


class RecipeCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    duration = fields.Integer(required=True, validate=lambda x: x > 0)
    servings_count = fields.Integer(required=True, validate=lambda x: x > 0, data_key='servingsCount')
    steps = fields.List(fields.Nested(RecipeStepSchema), required=True)
    categoryIds = fields.List(fields.UUID(), required=True)
    ingredientsIds = fields.List(fields.UUID(), required=True)


recipe_create_schema = RecipeCreateSchema()