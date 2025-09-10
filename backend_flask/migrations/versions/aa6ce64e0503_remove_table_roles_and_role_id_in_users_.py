"""remove table roles and role_id in users(on future will add this again)

Revision ID: aa6ce64e0503
Revises: 7377534a9221
Create Date: 2025-09-10 18:51:08.242206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa6ce64e0503'
down_revision = '7377534a9221'
branch_labels = None
depends_on = None


def upgrade():
    # спочатку прибираємо FK та колонку
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('users_role_id_fkey'), type_='foreignkey')
        batch_op.drop_column('role_id')

    # тепер можна видаляти таблицю roles
    op.drop_table('roles')


def downgrade():
    # створюємо таблицю roles спочатку
    op.create_table('roles',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.CheckConstraint('length(TRIM(BOTH FROM name)) > 0', name=op.f('ck_roles_name_required')),
        sa.PrimaryKeyConstraint('id', name=op.f('roles_pkey')),
        sa.UniqueConstraint('name', name=op.f('roles_name_key'), postgresql_include=[], postgresql_nulls_not_distinct=False)
    )

    # потім додаємо колонку role_id у users і FK
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.UUID(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key(batch_op.f('users_role_id_fkey'), 'roles', ['role_id'], ['id'])
