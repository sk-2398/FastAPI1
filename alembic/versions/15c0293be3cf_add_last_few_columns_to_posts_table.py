"""add last few columns to posts table

Revision ID: 15c0293be3cf
Revises: 369e6e7e54c3
Create Date: 2022-01-18 09:26:53.590241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15c0293be3cf'
down_revision = '369e6e7e54c3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_on',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_on')
    pass
