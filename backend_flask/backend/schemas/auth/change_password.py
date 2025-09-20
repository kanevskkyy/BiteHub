from marshmallow import Schema, fields, validates, validates_schema, ValidationError


class ChangePasswordSchema(Schema):
    old_password = fields.String(required=True, data_key='oldPassword')
    new_password = fields.String(required=True, data_key='newPassword')
    confirm_password = fields.String(required=True, data_key='confirmPassword')

    @validates('old_password')
    def validate_old_password(self, value: str, **kwargs):
        if value.strip() == '' or len(value.strip()) == 0:
            raise ValidationError('Old password cannot be empty')

    @validates('new_password')
    def validate_new_password(self, value: str, **kwargs):
        if value.strip() == '' or len(value.strip()) == 0:
            raise ValidationError('New password cannot be empty')

    @validates('confirm_password')
    def validate_confirm_password(self, value: str, **kwargs):
        if value.strip() == '' or len(value.strip()) == 0:
            raise ValidationError('Confirm password cannot be empty')


    @validates_schema
    def validate_password(self, data, **kwargs):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError(
                {
                    'confirm_password': ['Passwords do not match']
                })


change_password_schema = ChangePasswordSchema()