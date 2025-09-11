from marshmallow import Schema, fields, validate


class PaginationSchema(Schema):
    page = fields.Integer(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Integer(load_default=10, validate=validate.Range(min=1, max=100), data_key='perPage')


pagination_schema = PaginationSchema()