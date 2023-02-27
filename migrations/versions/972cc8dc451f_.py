"""empty message

Revision ID: 972cc8dc451f
Revises: 4062882056e0
Create Date: 2023-02-26 16:50:23.878585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '972cc8dc451f'
down_revision = '4062882056e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('joke',
    sa.Column('joke_id', sa.Integer(), nullable=False),
    sa.Column('joke', sa.String(), nullable=True),
    sa.Column('punchline', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('joke_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('joke_join',
    sa.Column('joke_id', sa.Integer(), nullable=True),
    sa.Column('User_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['User_id'], ['user.user_id'], ),
    sa.ForeignKeyConstraint(['joke_id'], ['joke.joke_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('joke_join')
    op.drop_table('user')
    op.drop_table('joke')
    # ### end Alembic commands ###