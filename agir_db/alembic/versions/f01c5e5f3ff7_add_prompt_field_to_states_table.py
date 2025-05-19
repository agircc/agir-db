"""Add prompt field to states table

Revision ID: f01c5e5f3ff7
Revises: fed1a5f2f5f2
Create Date: 2025-05-19 18:00:25.230200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f01c5e5f3ff7'
down_revision: Union[str, None] = 'fed1a5f2f5f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('states', sa.Column('prompt', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('states', 'prompt')
