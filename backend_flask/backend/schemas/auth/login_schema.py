from flask_restx import ValidationError
from marshmallow import Schema, fields, validates


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def validate_username(self, username: str, **kwargs) -> str:
        if username.strip() == '':
            raise ValidationError('Username cannot be empty')

        return username

    @validates('password')
    def validate_password(self, password: str, **kwargs) -> str:
        if password.strip() == '':
            raise ValidationError('Password cannot be empty')

        return password

login_schema = LoginSchema()