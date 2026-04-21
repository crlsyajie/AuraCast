"""Add action_plan to RecommendationLog

Revision ID: f91f467cbe07
Revises: 51cc3fbfaca9
Create Date: 2026-04-21 16:18:52.094138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f91f467cbe07'
down_revision: Union[str, Sequence[str], None] = '51cc3fbfaca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('recommendation_logs') as batch_op:
        batch_op.add_column(sa.Column('action_plan', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('recommendation_logs') as batch_op:
        batch_op.drop_column('action_plan')
