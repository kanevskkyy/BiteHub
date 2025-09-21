from marshmallow import Schema, fields, validates, ValidationError


class RecipeFilterSchema(Schema):
    page = fields.Integer(load_default=1, data_key='page')
    per_page = fields.Integer(load_default=24,data_key='perPage')
    user_id = fields.UUID(load_default=None, allow_none=True, data_key='userId')
    category_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='categoryIds')
    ingredient_ids = fields.List(fields.UUID(), load_default=[], allow_none=True, data_key='ingredientIds')
    mode = fields.String(load_default='or')

    @validates('page')
    def validate_page(self, page: int, **kwargs):
        if page < 1:
            raise ValidationError('Page must be greater than 0')

        return page

    @validates('per_page')
    def validate_per_page(self, per_page: int, **kwargs):
        if per_page < 1:
            raise ValidationError('Page must be greater than 0')
        if per_page > 100:
            raise ValidationError('Page must be less than 100')

        return per_page

    @validates('mode')
    def validate_mode(self, mode: str, **kwargs):
        if mode not in ('and', 'or'):
            raise ValidationError('Mode must be "and" or "or"')
        return mode


recipe_filter_schema = RecipeFilterSchema()