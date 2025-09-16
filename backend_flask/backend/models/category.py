from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import URLType

from backend.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(50), unique= True, nullable=False)
    icon_url = db.Column(URLType, nullable=False)

    recipe_categories = db.relationship(
        'RecipeCategory',
        back_populates='category',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    __table_args__ = (
        db.CheckConstraint('length(trim(name)) > 0', name='ck_categories_name_required'),
    )