"""empty message

Revision ID: 7b8fd78eada3
Revises: b3cf39668475
Create Date: 2022-11-30 21:54:54.795279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b8fd78eada3'
down_revision = 'b3cf39668475'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_booking')
    op.drop_table('event_db')
    op.drop_table('event')
    op.drop_table('venue_booking_db')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_booking_db',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('venueBookingId', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('venueNumber', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('venueName', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('bookingFee', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('maximumOccupancy', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bookedBy', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('venueBookedDate', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('venueBookingStart', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('venueBookingEnd', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='venue_booking_db_pkey')
    )
    op.create_table('event',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('eventNumber', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('eventName', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('entryFee', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('maximumOccupancy', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createdBy', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='event_pkey'),
    sa.UniqueConstraint('eventNumber', name='event_eventNumber_key')
    )
    op.create_table('event_db',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('eventNumber', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('eventName', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
    sa.Column('eventEntryFee', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('maximumOccupancy', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('createdBy', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('eventDate', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('eventStartTime', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('eventEndTime', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('graduationLevel', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='event_db_pkey'),
    sa.UniqueConstraint('eventNumber', name='event_db_eventNumber_key')
    )
    op.create_table('venue_booking',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('venueBookingId', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('venueNumber', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('venueName', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('bookingFee', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('maximumOccupancy', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('bookedBy', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('venueBookedDate', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('venueBookingStart', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.Column('venueBookingEnd', sa.VARCHAR(length=20), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='venue_booking_pkey'),
    sa.UniqueConstraint('venueNumber', name='venue_booking_venueNumber_key')
    )
    # ### end Alembic commands ###
