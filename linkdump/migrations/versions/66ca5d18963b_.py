"""empty message

Revision ID: 66ca5d18963b
Revises: e510de2bd585
Create Date: 2020-03-04 12:56:34.901166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66ca5d18963b'
down_revision = 'e510de2bd585'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_users_username', 'users', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_users_username', 'users', ['username'])
    # ### end Alembic commands ###
