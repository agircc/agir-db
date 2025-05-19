"""Change prompt to prompts array

Revision ID: d5527ed90f6b
Revises: f01c5e5f3ff7
Create Date: 2025-05-19 18:12:19.087479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd5527ed90f6b'
down_revision: Union[str, None] = 'f01c5e5f3ff7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing prompt column
    op.drop_column('states', 'prompt')
    # Add the new prompts array column
    op.add_column('states', sa.Column('prompts', postgresql.ARRAY(sa.Text()), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the prompts array column
    op.drop_column('states', 'prompts')
    # Add back the original prompt column
    op.add_column('states', sa.Column('prompt', sa.Text(), nullable=True))
