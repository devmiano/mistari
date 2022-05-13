"""changed category schemas

Revision ID: 4b1d514bc583
Revises: 4c4735eaab58
Create Date: 2022-05-11 01:33:11.285696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b1d514bc583'
down_revision = '4c4735eaab58'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    # ### end Alembic commands ###