"""update_recommendation_logs

Revision ID: 895f0e4e1247
Revises: 51cc3fbfaca9
Create Date: 2026-05-04 17:01:35.353545

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '895f0e4e1247'
down_revision: Union[str, Sequence[str], None] = '51cc3fbfaca9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('recommendation_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('action_plan', sa.String(), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('recommendations', sa.String(), nullable=False, server_default='[]'))
        batch_op.drop_column('recommendation')


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('recommendation_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recommendation', sa.VARCHAR(), nullable=False, server_default=''))
        batch_op.drop_column('recommendations')
        batch_op.drop_column('action_plan')
