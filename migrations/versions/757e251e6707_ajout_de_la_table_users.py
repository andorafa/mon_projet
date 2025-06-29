"""Ajout de la table users

Revision ID: 757e251e6707
Revises: 9b19b0e39cd0
Create Date: 2025-03-16 18:34:13.582908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '757e251e6707'
down_revision = '9b19b0e39cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('api_key', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_key'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
