"""add content column to posts table

Revision ID: 3f3ac93835d4
Revises: f95541d4afb7
Create Date: 2022-01-17 17:23:36.366016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f3ac93835d4'
down_revision = 'f95541d4afb7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
