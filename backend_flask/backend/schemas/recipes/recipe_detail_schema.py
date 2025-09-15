from marshmallow import Schema, fields

from backend.schemas.category_schema import CategorySchema
from backend.schemas.ingredient_schema import IngredientSchema
from backend.schemas.recipes.recipe_step_schema import RecipeStepSchema
from backend.schemas.users_schema.user_detail_schema import UserDetailSchema


class RecipeDetailSchema(Schema):
    id = fields.UUID(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    duration = fields.Int(required=True)
    image_url = fields.Str(dump_only=True, data_key='imageUrl')
    servings_count = fields.Int(required=True, data_key='servingsCount')
    created_at = fields.DateTime(dump_only=True, data_key='createdAt')

    author = fields.Nested(UserDetailSchema, dump_only=True, only=('id', 'username', 'avatar_url'))

    steps = fields.List(fields.Nested(RecipeStepSchema), dump_only=True)
    ingredients = fields.List(fields.Nested(IngredientSchema), dump_only=True)
    categories = fields.List(fields.Nested(CategorySchema, only=('id', 'name')), dump_only=True)


recipe_detail_schema = RecipeDetailSchema()
recipes_detail_schema = RecipeDetailSchema(many=True)
