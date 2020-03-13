"""empty message

Revision ID: bbf3daf3b5d0
Revises: 3168769e5656
Create Date: 2020-03-14 06:09:23.387712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbf3daf3b5d0'
down_revision = '3168769e5656'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('politician', sa.Column('avatar_url', sa.String(length=100), nullable=True))
    op.drop_column('politician', 'politician_avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('politician', sa.Column('politician_avatar', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('politician', 'avatar_url')
    # ### end Alembic commands ###
