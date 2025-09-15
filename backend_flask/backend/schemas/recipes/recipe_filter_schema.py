from marshmallow import Schema, fields


class RecipeFilterSchema(Schema):
    page = fields.Integer(load_default=1, validate=lambda x: x > 0, data_key='page')
    per_page = fields.Integer(load_default=24, validate=lambda x: 0 < x <= 100, data_key='perPage')
    user_id = fields.UUID(load_default=None, allow_none=True, data_key='userId')
    category_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='categoryIds')
    ingredient_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='ingredientIds')


recipe_filter_schema = RecipeFilterSchema()