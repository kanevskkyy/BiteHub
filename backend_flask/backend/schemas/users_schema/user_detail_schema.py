from marshmallow import Schema, fields


class UserDetailSchema(Schema):
    id = fields.UUID(required=True)
    username = fields.String(required=True)
    description = fields.String(required=True)
    first_name = fields.String(required=True, data_key='firstName')
    last_name = fields.String(required=True, data_key='lastName')
    created_at = fields.DateTime(required=True, data_key='createdAt')
    avatar_url= fields.String(required=True, data_key='avatarUrl')

user_detail_schema = UserDetailSchema()