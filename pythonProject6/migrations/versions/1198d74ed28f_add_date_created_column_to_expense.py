"""Add date_created column to Expense

Revision ID: 1198d74ed28f
Revises: f6adddcda9dd
Create Date: 2023-08-10 21:14:51.456054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1198d74ed28f'
down_revision = 'f6adddcda9dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))

    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.drop_column('date_created')

    with op.batch_alter_table('expense', schema=None) as batch_op:
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###
