"""removed creator_id attribute in Schedule model

Revision ID: b9ccf87c15b9
Revises: 2f99710c13a9
Create Date: 2024-08-06 12:49:00.324492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9ccf87c15b9'
down_revision: Union[str, None] = '2f99710c13a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_schedule_creator_id_user', 'schedule', type_='foreignkey')
    op.drop_column('schedule', 'creator_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule', sa.Column('creator_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('fk_schedule_creator_id_user', 'schedule', 'user', ['creator_id'], ['id'])
    # ### end Alembic commands ###