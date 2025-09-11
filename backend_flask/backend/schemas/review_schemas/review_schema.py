from marshmallow import Schema, fields, ValidationError, validates

from backend.schemas.users_schema.user_detail_schema import UserDetailSchema


class ReviewSchema(Schema):
    id = fields.UUID(dump_only=True)
    rating = fields.Integer()
    comment = fields.String()
    created_at = fields.DateTime(dump_only=True, data_key='createdAt')
    user_id = fields.UUID(load_only=True, required=True, data_key='userId')
    recipe_id = fields.UUID(load_only=True, required=True, data_key='recipeId')
    user = fields.Nested(UserDetailSchema, only=('id', 'username', 'avatar_url'), dump_only=True)

    @validates('rating')
    def validate_rating(self, value: int, **kwargs) -> int:
        if value < 0 or value > 5:
            raise ValidationError('Rating must be between 0 and 5')

        return value

    @validates('comment')
    def validate_comment(self, value: str, **kwargs) -> str:
        if not value.strip():
            raise ValidationError('Comment cannot be empty')

        return value


review_schema = ReviewSchema()
review_list_schema = ReviewSchema(many=True)