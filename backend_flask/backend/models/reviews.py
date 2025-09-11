from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db


class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = db.Column(UUID, db.ForeignKey('users.id'))
    recipe_id = db.Column(UUID, db.ForeignKey('recipes.id'))
    rating = db.Column(db.Integer, default=1, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    user = db.relationship('User', backref='ratings', foreign_keys=[user_id])
    recipe = db.relationship('Recipe', backref='ratings', foreign_keys=[recipe_id])

    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='uq_reviews_user_id_recipe_id'),
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_ratings_rating_valid'),
        db.CheckConstraint('length(trim(comment)) > 0', name='ck_ratings_comment_required'),
    )