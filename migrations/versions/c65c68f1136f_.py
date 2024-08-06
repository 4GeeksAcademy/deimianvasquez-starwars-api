"""empty message

Revision ID: c65c68f1136f
Revises: 
Create Date: 2024-08-06 01:47:41.434439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c65c68f1136f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('height', sa.String(length=100), nullable=False),
    sa.Column('mass', sa.String(length=100), nullable=False),
    sa.Column('hair_color', sa.String(length=100), nullable=False),
    sa.Column('skin_color', sa.String(length=100), nullable=False),
    sa.Column('eye_color', sa.String(length=100), nullable=False),
    sa.Column('birth_year', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullname', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('people')
    # ### end Alembic commands ###