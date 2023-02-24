"""empty message

Revision ID: 8772e511a760
Revises: 3f376f77388e
Create Date: 2023-02-23 20:51:09.176592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8772e511a760'
down_revision = '3f376f77388e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('joke', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('joke', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
