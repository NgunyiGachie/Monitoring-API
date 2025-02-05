"""Initial migration

Revision ID: b5cd4c0e7f09
Revises: 
Create Date: 2025-02-05 21:41:53.195145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5cd4c0e7f09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=False),
    sa.Column('_password_hash', sa.VARCHAR(), nullable=False),
    sa.Column('image_url', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###
