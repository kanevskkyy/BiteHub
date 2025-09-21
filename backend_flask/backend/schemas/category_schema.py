from marshmallow import Schema, fields, validates, ValidationError


class CategorySchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    icon_url = fields.String(dump_only=True, data_key='iconUrl')

    @validates('name')
    def validate_name(self, name: str, **kwargs) -> str:
        if name.strip() == '':
            raise ValidationError('Name cannot be empty')

        if len(name.strip()) > 50:
            raise ValidationError('Name cannot be longer than 50 characters')

        return name


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)