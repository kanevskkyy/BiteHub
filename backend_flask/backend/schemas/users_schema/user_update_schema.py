from marshmallow import Schema, fields, validates, ValidationError


class UserUpdateSchema(Schema):
    username = fields.String(required=True)
    description = fields.String(required=False, load_default=None)
    first_name = fields.String(required=True, data_key='firstName')
    last_name = fields.String(required=True, data_key='lastName')

    @validates('username')
    def validate_username(self, username: str, **kwargs) -> str:
        if username.strip() == '':
            raise ValidationError('Username cannot be empty')
        if len(username.strip()) > 100:
            raise ValidationError('Username cannot be longer than 100 characters')

        return username

    @validates('first_name')
    def validate_first_name(self, first_name: str, **kwargs) -> str:
        if first_name.strip() == '':
            raise ValidationError('First name cannot be empty')
        if len(first_name.strip()) > 100:
            raise ValidationError('First name cannot be longer than 100 characters')

        return first_name

    @validates('last_name')
    def validate_last_name(self, last_name: str, **kwargs) -> str:
        if last_name.strip() == '':
            raise ValidationError('Last name cannot be empty')
        if len(last_name.strip()) > 100:
            raise ValidationError('Last name cannot be longer than 100 characters')

        return last_name


user_update_schema = UserUpdateSchema()