from marshmallow import Schema, fields


class TokenSchema(Schema):
    accessToken = fields.String(required=True, data_key='accessToken')
    refreshToken = fields.String(required=True, data_key='refreshToken')


token_schema = TokenSchema()