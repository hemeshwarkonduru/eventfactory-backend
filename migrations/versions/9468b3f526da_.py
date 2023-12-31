"""empty message

Revision ID: 9468b3f526da
Revises: b0247fbb0561
Create Date: 2022-12-01 22:09:52.210182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9468b3f526da'
down_revision = 'b0247fbb0561'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('event_booking')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('eventsAttending', sa.PickleType(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('eventsAttending')

    op.create_table('event_booking',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('eventBookingId', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('eventNumber', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('eventEntryFee', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('maximumOccupancy', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createdBy', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('eventDate', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('eventStartTime', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('eventEndTime', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('venueNumber', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('graduationLevel', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='event_booking_pkey'),
    sa.UniqueConstraint('eventNumber', name='event_booking_eventNumber_key')
    )
    # ### end Alembic commands ###
