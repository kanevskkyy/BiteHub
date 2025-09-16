from marshmallow import Schema, fields, validates


class RecipeFilterSchema(Schema):
    page = fields.Integer(load_default=1, data_key='page')
    per_page = fields.Integer(load_default=24,data_key='perPage')
    user_id = fields.UUID(load_default=None, allow_none=True, data_key='userId')
    category_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='categoryIds')
    ingredient_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='ingredientIds')

    @validates('page')
    def validate_page(self, page: int, **kwargs):
        if page < 1:
            raise ValueError('Page must be greater than 0')

        return page

    @validates('per_page')
    def validate_per_page(self, per_page: int, **kwargs):
        if per_page < 1:
            raise ValueError('Page must be greater than 0')
        if per_page > 100:
            raise ValueError('Page must be less than 100')

        return per_page



recipe_filter_schema = RecipeFilterSchema()