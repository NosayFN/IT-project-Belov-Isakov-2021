"""empty message

Revision ID: 2d43c7456304
Revises: 2a316a46d31d
Create Date: 2022-02-06 14:45:23.711622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d43c7456304'
down_revision = '2a316a46d31d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('telegram_id', sa.String(), nullable=True))
    op.add_column('users', sa.Column('telegram_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'telegram_name')
    op.drop_column('users', 'telegram_id')
    # ### end Alembic commands ###
