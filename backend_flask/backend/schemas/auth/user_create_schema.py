from marshmallow import (Schema, fields, validates,
                         ValidationError,
                         validates_schema)

class UserCreateSchema(Schema):
    username = fields.String(required=True)
    description = fields.String(required=False, load_default=None)
    first_name = fields.String(required=True, data_key='firstName')
    last_name = fields.String(required=True, data_key='lastName')
    password_hash = fields.String(required=True, data_key='password')
    confirm_password = fields.String(required=True, load_only=True, data_key='confirmPassword')

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

    @validates('password_hash')
    def validate_password(self, password: str, **kwargs) -> str:
        if password.strip() == '':
            raise ValidationError('Password cannot be empty')
        if len(password.strip()) < 6:
            raise ValidationError('Password must be at least 6 characters')

        if not any(char.isdigit() for char in password):
            raise ValidationError('Password must contain at least one digit')

        return password

    @validates_schema
    def validate_password_match(self, data, **kwargs):
        if data.get('password_hash') != data.get('confirm_password'):
            raise ValidationError('Passwords do not match!')


user_create_schema = UserCreateSchema()