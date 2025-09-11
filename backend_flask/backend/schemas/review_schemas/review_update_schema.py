from marshmallow import Schema, fields, validates, ValidationError


class ReviewUpdateSchema(Schema):
    rating = fields.Integer()
    comment = fields.String()

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


review_update_schema = ReviewUpdateSchema()