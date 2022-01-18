"""add foreign-key to posts table

Revision ID: 369e6e7e54c3
Revises: e62016e1f65d
Create Date: 2022-01-17 17:52:18.882165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369e6e7e54c3'
down_revision = 'e62016e1f65d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('auther_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',
                          local_cols=['auther_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','auther_id')
    pass
