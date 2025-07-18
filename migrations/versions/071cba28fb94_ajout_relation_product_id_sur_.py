"""Ajout relation product_id sur OrderProduct

Revision ID: 071cba28fb94
Revises: 
Create Date: 2025-06-30 23:11:03.265661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '071cba28fb94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    with op.batch_alter_table('order_product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'product', ['product_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order_product', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('product_id')

    op.create_table('users',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('api_key', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('api_key', name='users_api_key_key'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    # ### end Alembic commands ###
