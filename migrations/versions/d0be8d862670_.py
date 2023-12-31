"""empty message

Revision ID: d0be8d862670
Revises: ce802fb0b05f
Create Date: 2022-12-04 01:12:41.849863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0be8d862670'
down_revision = 'ce802fb0b05f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_db', schema=None) as batch_op:
        batch_op.add_column(sa.Column('waitList', sa.PickleType(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_db', schema=None) as batch_op:
        batch_op.drop_column('waitList')

    # ### end Alembic commands ###
