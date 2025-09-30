from marshmallow import Schema, fields, validates, ValidationError


class PaginationSchema(Schema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(load_default=10, data_key='perPage')

    @validates('page')
    def validate_page(self, value:int, **kwargs):
        if value < 1:
            raise ValidationError('Page must be greater than 1')

        return value

    @validates('per_page')
    def validate_per_page(self, value:int, **kwargs):
        if value < 1 or value > 100:
            raise ValidationError('Page must be between 1 and 100')

        return value

pagination_schema = PaginationSchema()