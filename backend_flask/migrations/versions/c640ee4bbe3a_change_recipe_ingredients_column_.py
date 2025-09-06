"""Change recipe-ingredients column quantity type from float to string

Revision ID: c640ee4bbe3a
Revises: e153a8f28f5f
Create Date: 2025-09-06 17:00:59.864863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c640ee4bbe3a'
down_revision = 'e153a8f28f5f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "ck_recipe_ingredients_quantity_valid",
        "recipe_ingredients",
        type_="check"
    )
    with op.batch_alter_table("recipe_ingredients", schema=None) as batch_op:
        batch_op.alter_column(
            "quantity",
            existing_type=sa.Float(),
            type_=sa.String(length=40),
            postgresql_using="quantity::text"
        )


def downgrade():

    with op.batch_alter_table("recipe_ingredients", schema=None) as batch_op:
        batch_op.alter_column(
            "quantity",
            existing_type=sa.String(length=40),
            type_=sa.Float(),
            postgresql_using="quantity::double precision"
        )
    op.create_check_constraint(
        "ck_recipe_ingredients_quantity_valid",
        "recipe_ingredients",
        "quantity > 0"
    )