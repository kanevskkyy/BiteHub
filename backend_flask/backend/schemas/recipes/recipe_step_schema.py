from marshmallow import Schema, fields, validate


class RecipeStepSchema(Schema):
    id = fields.UUID(dump_only=True)
    step_number = fields.Integer(required=True, validate=lambda x: x > 0, data_key='stepNumber')
    description = fields.Str(required=True, validate=validate.Length(min=1))