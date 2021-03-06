"""Added new column to memo model

Revision ID: c9156ccec844
Revises: b196fd7932f7
Create Date: 2022-04-14 11:10:57.524025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9156ccec844'
down_revision = 'b196fd7932f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('memo', sa.Column('is_deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('memo', 'is_deleted')
    # ### end Alembic commands ###
