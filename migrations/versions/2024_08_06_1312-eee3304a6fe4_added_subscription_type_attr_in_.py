"""added subscription_type attr in subscription model

Revision ID: eee3304a6fe4
Revises: b9ccf87c15b9
Create Date: 2024-08-06 13:12:19.560094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eee3304a6fe4'
down_revision: Union[str, None] = 'b9ccf87c15b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE subscription_type AS ENUM ('OWNER', 'FOLLOWER');")
    op.add_column('subscription', sa.Column('subscription_type', sa.Enum('OWNER', 'FOLLOWER', name='subscription_type'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscription', 'subscription_type')
    # ### end Alembic commands ###