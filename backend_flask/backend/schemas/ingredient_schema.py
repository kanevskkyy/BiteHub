from flask_restx import ValidationError
from marshmallow import Schema, fields, validates, post_load

from backend.models import Ingredients


class IngredientSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    icon_url = fields.String(dump_only=True, data_key='iconUrl')

    @validates('name')
    def validate_name(self, name: str, **kwargs) -> str:
        if name.strip() == '':
            raise ValidationError('Name cannot be empty')
        if len(name.strip()) > 100:
            raise ValidationError('Name must be less than 100 characters')

        return name


ingredient_schema = IngredientSchema()
ingredients_schema = IngredientSchema(many=True)