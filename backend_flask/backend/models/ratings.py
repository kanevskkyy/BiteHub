from sqlalchemy.dialects.postgresql import UUID

from backend.extensions import db


class Rating(db.Model):
    __tablename__ = 'ratings'

    user_id = db.Column(UUID, db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(UUID, db.ForeignKey('recipes.id'), primary_key=True)
    rating = db.Column(db.Integer, default=1, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())

    users = db.relationship('User', backref='ratings', foreign_keys=[user_id])
    recipes = db.relationship('Recipe', backref='ratings', foreign_keys=[recipe_id])

    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_ratings_rating_valid'),
        db.CheckConstraint('length(trim(comment)) > 0', name='ck_ratings_comment_required'),
    )