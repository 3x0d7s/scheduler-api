"""follow_entry renamed to subscription

Revision ID: 17e34ab26857
Revises: 46b5b2c894e3
Create Date: 2024-06-27 20:10:27.702456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '17e34ab26857'
down_revision: Union[str, None] = '46b5b2c894e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], name=op.f('fk_subscription_schedule_id_schedule')),
    sa.ForeignKeyConstraint(['subscriber_id'], ['user.id'], name=op.f('fk_subscription_subscriber_id_user')),
    sa.PrimaryKeyConstraint('subscriber_id', 'schedule_id', 'id', name=op.f('pk_subscription')),
    sa.UniqueConstraint('schedule_id', name=op.f('uq_subscription_schedule_id')),
    sa.UniqueConstraint('subscriber_id', name=op.f('uq_subscription_subscriber_id'))
    )
    op.create_table('schedule_association',
    sa.Column('schedule_id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], name=op.f('fk_schedule_association_schedule_id_schedule')),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscription.schedule_id'], name=op.f('fk_schedule_association_subscription_id_subscription')),
    sa.PrimaryKeyConstraint('schedule_id', 'subscription_id', 'id', name=op.f('pk_schedule_association'))
    )
    op.create_table('subscriber_association',
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['user.id'], name=op.f('fk_subscriber_association_subscriber_id_user')),
    sa.ForeignKeyConstraint(['subscription_id'], ['subscription.subscriber_id'], name=op.f('fk_subscriber_association_subscription_id_subscription')),
    sa.PrimaryKeyConstraint('subscriber_id', 'subscription_id', 'id', name=op.f('pk_subscriber_association'))
    )
    op.drop_table('follower_association')
    op.drop_table('followed_association')
    op.drop_table('follow_entry')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow_entry',
    sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('followed_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text("timezone('utc'::text, now())"), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('follow_entry_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['schedule.id'], name='fk_follow_entry_followed_id_schedule'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='fk_follow_entry_follower_id_user'),
    sa.PrimaryKeyConstraint('id', name='pk_follow_entry'),
    sa.UniqueConstraint('followed_id', name='uq_follow_entry_followed_id'),
    sa.UniqueConstraint('follower_id', name='uq_follow_entry_follower_id'),
    postgresql_ignore_search_path=False
    )
    op.create_table('followed_association',
    sa.Column('followed_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('follow_entry_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['follow_entry_id'], ['follow_entry.followed_id'], name='fk_followed_association_follow_entry_id_follow_entry'),
    sa.ForeignKeyConstraint(['followed_id'], ['schedule.id'], name='fk_followed_association_followed_id_schedule'),
    sa.PrimaryKeyConstraint('followed_id', 'follow_entry_id', name='pk_followed_association')
    )
    op.create_table('follower_association',
    sa.Column('follower_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('follow_entry_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['follow_entry_id'], ['follow_entry.follower_id'], name='fk_follower_association_follow_entry_id_follow_entry'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='fk_follower_association_follower_id_user'),
    sa.PrimaryKeyConstraint('follower_id', 'follow_entry_id', name='pk_follower_association')
    )
    op.drop_table('subscriber_association')
    op.drop_table('schedule_association')
    op.drop_table('subscription')
    # ### end Alembic commands ###
