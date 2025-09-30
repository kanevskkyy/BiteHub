from marshmallow import Schema, fields, validates, ValidationError


class RecipeStepSchema(Schema):
    id = fields.UUID(dump_only=True)
    step_number = fields.Integer(required=True, data_key='stepNumber')
    description = fields.Str(required=True)

    @validates('step_number')
    def validate_step_number(self, step_number: int, **kwargs) -> int:
        if step_number < 1:
            raise ValidationError('step_number must be greater than 0')

        return step_number

    @validates('description')
    def validate_description(self, description: str, **kwargs) -> str:
        if description.strip() == '':
            raise ValidationError('description cannot be empty')

        return description