"""rename tables: users->assistants, agent_assignments->assistant_assignments, agent_roles->assistant_roles

Revision ID: 65dc01ffca4c
Revises: abc123def456
Create Date: 2025-07-05 10:55:39.663249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '65dc01ffca4c'
down_revision: Union[str, None] = 'abc123def456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Step 1: Rename tables
    op.execute('ALTER TABLE agent_roles RENAME TO assistant_roles')
    op.execute('ALTER TABLE agent_assignments RENAME TO assistant_assignments')
    
    # Step 2: Rename column in state_roles table
    op.execute('ALTER TABLE state_roles RENAME COLUMN agent_role_id TO assistant_role_id')
    
    # Step 3: Update index names for assistants table (formerly users)
    op.drop_index(op.f('ix_users_email'), table_name='assistants')
    op.drop_index(op.f('ix_users_first_name'), table_name='assistants')
    op.drop_index(op.f('ix_users_id'), table_name='assistants')
    op.drop_index(op.f('ix_users_last_name'), table_name='assistants')
    op.drop_index(op.f('ix_users_username'), table_name='assistants')
    op.create_index(op.f('ix_assistants_email'), 'assistants', ['email'], unique=True)
    op.create_index(op.f('ix_assistants_first_name'), 'assistants', ['first_name'], unique=False)
    op.create_index(op.f('ix_assistants_id'), 'assistants', ['id'], unique=False)
    op.create_index(op.f('ix_assistants_last_name'), 'assistants', ['last_name'], unique=False)
    op.create_index(op.f('ix_assistants_username'), 'assistants', ['username'], unique=True)
    
    # Step 4: Update index names for assistant_assignments table
    op.drop_index('ix_agent_assignments_assistant_id', table_name='assistant_assignments')
    op.drop_index('ix_agent_assignments_episode_id', table_name='assistant_assignments')
    op.drop_index('ix_agent_assignments_id', table_name='assistant_assignments')
    op.create_index(op.f('ix_assistant_assignments_assistant_id'), 'assistant_assignments', ['assistant_id'], unique=False)
    op.create_index(op.f('ix_assistant_assignments_episode_id'), 'assistant_assignments', ['episode_id'], unique=False)
    op.create_index(op.f('ix_assistant_assignments_id'), 'assistant_assignments', ['id'], unique=False)
    
    # Step 5: Update index names for assistant_roles table
    op.drop_index('ix_agent_roles_name', table_name='assistant_roles')
    op.create_index(op.f('ix_assistant_roles_name'), 'assistant_roles', ['name'], unique=False)
    
    # Step 6: Update index names for other renamed tables
    op.drop_index(op.f('ix_user_capabilities_id'), table_name='assistant_capabilities')
    op.drop_index(op.f('ix_user_capabilities_name'), table_name='assistant_capabilities')
    op.create_index(op.f('ix_assistant_capabilities_id'), 'assistant_capabilities', ['id'], unique=False)
    op.create_index(op.f('ix_assistant_capabilities_name'), 'assistant_capabilities', ['name'], unique=False)
    
    op.drop_index(op.f('ix_user_memories_id'), table_name='assistant_memories')
    op.create_index(op.f('ix_assistant_memories_id'), 'assistant_memories', ['id'], unique=False)
    
    op.drop_index(op.f('ix_user_organizations_id'), table_name='assistant_organizations')
    op.drop_index(op.f('ix_user_organizations_organization_id'), table_name='assistant_organizations')
    op.create_index(op.f('ix_assistant_organizations_id'), 'assistant_organizations', ['id'], unique=False)
    op.create_index(op.f('ix_assistant_organizations_organization_id'), 'assistant_organizations', ['organization_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse the operations from upgrade
    
    # Step 1: Revert index names for other tables
    op.drop_index(op.f('ix_assistant_organizations_organization_id'), table_name='assistant_organizations')
    op.drop_index(op.f('ix_assistant_organizations_id'), table_name='assistant_organizations')
    op.create_index(op.f('ix_user_organizations_organization_id'), 'assistant_organizations', ['organization_id'], unique=False)
    op.create_index(op.f('ix_user_organizations_id'), 'assistant_organizations', ['id'], unique=False)
    
    op.drop_index(op.f('ix_assistant_memories_id'), table_name='assistant_memories')
    op.create_index(op.f('ix_user_memories_id'), 'assistant_memories', ['id'], unique=False)
    
    op.drop_index(op.f('ix_assistant_capabilities_name'), table_name='assistant_capabilities')
    op.drop_index(op.f('ix_assistant_capabilities_id'), table_name='assistant_capabilities')
    op.create_index(op.f('ix_user_capabilities_name'), 'assistant_capabilities', ['name'], unique=False)
    op.create_index(op.f('ix_user_capabilities_id'), 'assistant_capabilities', ['id'], unique=False)
    
    # Step 2: Revert index names for assistant_roles table
    op.drop_index(op.f('ix_assistant_roles_name'), table_name='assistant_roles')
    op.create_index('ix_agent_roles_name', 'assistant_roles', ['name'], unique=False)
    
    # Step 3: Revert index names for assistant_assignments table
    op.drop_index(op.f('ix_assistant_assignments_assistant_id'), table_name='assistant_assignments')
    op.drop_index(op.f('ix_assistant_assignments_episode_id'), table_name='assistant_assignments')
    op.drop_index(op.f('ix_assistant_assignments_id'), table_name='assistant_assignments')
    op.create_index('ix_agent_assignments_assistant_id', 'assistant_assignments', ['assistant_id'], unique=False)
    op.create_index('ix_agent_assignments_episode_id', 'assistant_assignments', ['episode_id'], unique=False)
    op.create_index('ix_agent_assignments_id', 'assistant_assignments', ['id'], unique=False)
    
    # Step 4: Revert index names for assistants table
    op.drop_index(op.f('ix_assistants_username'), table_name='assistants')
    op.drop_index(op.f('ix_assistants_last_name'), table_name='assistants')
    op.drop_index(op.f('ix_assistants_id'), table_name='assistants')
    op.drop_index(op.f('ix_assistants_first_name'), table_name='assistants')
    op.drop_index(op.f('ix_assistants_email'), table_name='assistants')
    op.create_index(op.f('ix_users_username'), 'assistants', ['username'], unique=True)
    op.create_index(op.f('ix_users_last_name'), 'assistants', ['last_name'], unique=False)
    op.create_index(op.f('ix_users_id'), 'assistants', ['id'], unique=False)
    op.create_index(op.f('ix_users_first_name'), 'assistants', ['first_name'], unique=False)
    op.create_index(op.f('ix_users_email'), 'assistants', ['email'], unique=True)
    
    # Step 5: Revert column name in state_roles table
    op.execute('ALTER TABLE state_roles RENAME COLUMN assistant_role_id TO agent_role_id')
    
    # Step 6: Revert table names
    op.execute('ALTER TABLE assistant_assignments RENAME TO agent_assignments')
    op.execute('ALTER TABLE assistant_roles RENAME TO agent_roles')
