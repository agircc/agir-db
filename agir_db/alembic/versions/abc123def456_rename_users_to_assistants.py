"""rename users to assistants

Revision ID: abc123def456
Revises: 346645a27776
Create Date: 2025-07-04 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc123def456'
down_revision: Union[str, None] = '346645a27776'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # Step 1: Rename the main users table to assistants
    op.rename_table('users', 'assistants')
    
    # Step 2: Update all foreign key constraints to point to the new assistants table
    # (We need to do this before renaming other tables that reference users)
    
    # Update self-referencing foreign key in assistants table
    op.drop_constraint('users_created_by_fkey', 'assistants', type_='foreignkey')
    op.create_foreign_key('assistants_created_by_fkey', 'assistants', 'assistants', ['created_by'], ['id'])
    
    # Update tasks table
    op.drop_constraint('tasks_created_by_fkey', 'tasks', type_='foreignkey')
    op.drop_constraint('tasks_assigned_to_fkey', 'tasks', type_='foreignkey')
    op.drop_constraint('tasks_assigned_by_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_created_by_fkey', 'tasks', 'assistants', ['created_by'], ['id'])
    op.create_foreign_key('tasks_assigned_to_fkey', 'tasks', 'assistants', ['assigned_to'], ['id'])
    op.create_foreign_key('tasks_assigned_by_fkey', 'tasks', 'assistants', ['assigned_by'], ['id'])
    
    # Update task_comments table
    op.drop_constraint('task_comments_user_id_fkey', 'task_comments', type_='foreignkey')
    op.alter_column('task_comments', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('task_comments_assistant_id_fkey', 'task_comments', 'assistants', ['assistant_id'], ['id'])
    
    # Update task_attachments table
    op.drop_constraint('task_attachments_user_id_fkey', 'task_attachments', type_='foreignkey')
    op.alter_column('task_attachments', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('task_attachments_assistant_id_fkey', 'task_attachments', 'assistants', ['assistant_id'], ['id'])
    
    # Update chat_conversations table
    op.drop_constraint('chat_conversations_created_by_fkey', 'chat_conversations', type_='foreignkey')
    op.create_foreign_key('chat_conversations_created_by_fkey', 'chat_conversations', 'assistants', ['created_by'], ['id'])
    
    # Update chat_messages table
    op.drop_constraint('chat_messages_sender_id_fkey', 'chat_messages', type_='foreignkey')
    op.create_foreign_key('chat_messages_sender_id_fkey', 'chat_messages', 'assistants', ['sender_id'], ['id'])
    
    # Update chat_participants table
    op.drop_constraint('chat_participants_user_id_fkey', 'chat_participants', type_='foreignkey')
    op.drop_constraint('uq_participant_conversation_user', 'chat_participants', type_='unique')
    op.alter_column('chat_participants', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('chat_participants_assistant_id_fkey', 'chat_participants', 'assistants', ['assistant_id'], ['id'])
    op.create_unique_constraint('uq_participant_conversation_assistant', 'chat_participants', ['conversation_id', 'assistant_id'])
    
    # Update custom_fields table
    op.drop_constraint('custom_fields_user_id_fkey', 'custom_fields', type_='foreignkey')
    op.alter_column('custom_fields', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('custom_fields_assistant_id_fkey', 'custom_fields', 'assistants', ['assistant_id'], ['id'])
    
    # Update scenarios table
    op.drop_constraint('scenarios_created_by_fkey', 'scenarios', type_='foreignkey')
    op.create_foreign_key('scenarios_created_by_fkey', 'scenarios', 'assistants', ['created_by'], ['id'])
    
    # Update episodes table
    op.drop_constraint('episodes_initiator_id_fkey', 'episodes', type_='foreignkey')
    op.create_foreign_key('episodes_initiator_id_fkey', 'episodes', 'assistants', ['initiator_id'], ['id'])
    
    # Update steps table
    op.drop_constraint('steps_user_id_fkey', 'steps', type_='foreignkey')
    op.alter_column('steps', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('steps_assistant_id_fkey', 'steps', 'assistants', ['assistant_id'], ['id'])
    
    # Update agent_assignments table
    op.drop_constraint('agent_assignments_user_id_fkey', 'agent_assignments', type_='foreignkey')
    op.alter_column('agent_assignments', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('agent_assignments_assistant_id_fkey', 'agent_assignments', 'assistants', ['assistant_id'], ['id'])
    
    # Update organizations table
    op.drop_constraint('organizations_created_by_fkey', 'organizations', type_='foreignkey')
    op.create_foreign_key('organizations_created_by_fkey', 'organizations', 'assistants', ['created_by'], ['id'])
    
    # Step 3: Now rename the related tables and update their columns
    
    # Rename user_capabilities table to assistant_capabilities and update columns
    op.drop_constraint('user_capabilities_user_id_fkey', 'user_capabilities', type_='foreignkey')
    op.rename_table('user_capabilities', 'assistant_capabilities')
    op.alter_column('assistant_capabilities', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('assistant_capabilities_assistant_id_fkey', 'assistant_capabilities', 'assistants', ['assistant_id'], ['id'])
    
    # Rename user_memories table to assistant_memories and update columns
    op.drop_constraint('user_memories_user_id_fkey', 'user_memories', type_='foreignkey')
    op.rename_table('user_memories', 'assistant_memories')
    op.alter_column('assistant_memories', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('assistant_memories_assistant_id_fkey', 'assistant_memories', 'assistants', ['assistant_id'], ['id'])
    
    # Rename user_organizations table to assistant_organizations and update columns
    op.drop_constraint('user_organizations_user_id_fkey', 'user_organizations', type_='foreignkey')
    op.drop_constraint('user_organizations_added_by_fkey', 'user_organizations', type_='foreignkey')
    op.rename_table('user_organizations', 'assistant_organizations')
    op.alter_column('assistant_organizations', 'user_id', new_column_name='assistant_id')
    op.create_foreign_key('assistant_organizations_assistant_id_fkey', 'assistant_organizations', 'assistants', ['assistant_id'], ['id'])
    op.create_foreign_key('assistant_organizations_added_by_fkey', 'assistant_organizations', 'assistants', ['added_by'], ['id'])
    
    # Step 4: Update indexes to reflect new column names
    op.drop_index('ix_user_capabilities_user_id', table_name='assistant_capabilities')
    op.create_index('ix_assistant_capabilities_assistant_id', 'assistant_capabilities', ['assistant_id'])
    
    op.drop_index('ix_user_memories_user_id', table_name='assistant_memories')
    op.create_index('ix_assistant_memories_assistant_id', 'assistant_memories', ['assistant_id'])
    
    op.drop_index('ix_user_organizations_user_id', table_name='assistant_organizations')
    op.create_index('ix_assistant_organizations_assistant_id', 'assistant_organizations', ['assistant_id'])
    
    op.drop_index('ix_custom_fields_user_id', table_name='custom_fields')
    op.create_index('ix_custom_fields_assistant_id', 'custom_fields', ['assistant_id'])
    
    op.drop_index('ix_agent_assignments_user_id', table_name='agent_assignments')
    op.create_index('ix_agent_assignments_assistant_id', 'agent_assignments', ['assistant_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse all the changes in the opposite order
    
    # Revert indexes
    op.drop_index('ix_agent_assignments_assistant_id', table_name='agent_assignments')
    op.create_index('ix_agent_assignments_user_id', 'agent_assignments', ['assistant_id'])
    
    op.drop_index('ix_custom_fields_assistant_id', table_name='custom_fields')
    op.create_index('ix_custom_fields_user_id', 'custom_fields', ['assistant_id'])
    
    op.drop_index('ix_assistant_organizations_assistant_id', table_name='assistant_organizations')
    op.create_index('ix_user_organizations_user_id', 'assistant_organizations', ['assistant_id'])
    
    op.drop_index('ix_assistant_memories_assistant_id', table_name='assistant_memories')
    op.create_index('ix_user_memories_user_id', 'assistant_memories', ['assistant_id'])
    
    op.drop_index('ix_assistant_capabilities_assistant_id', table_name='assistant_capabilities')
    op.create_index('ix_user_capabilities_user_id', 'assistant_capabilities', ['assistant_id'])
    
    # Revert table renames and column renames
    op.drop_constraint('assistant_organizations_added_by_fkey', 'assistant_organizations', type_='foreignkey')
    op.drop_constraint('assistant_organizations_assistant_id_fkey', 'assistant_organizations', type_='foreignkey')
    op.alter_column('assistant_organizations', 'assistant_id', new_column_name='user_id')
    op.rename_table('assistant_organizations', 'user_organizations')
    op.create_foreign_key('user_organizations_user_id_fkey', 'user_organizations', 'assistants', ['user_id'], ['id'])
    op.create_foreign_key('user_organizations_added_by_fkey', 'user_organizations', 'assistants', ['added_by'], ['id'])
    
    op.drop_constraint('assistant_memories_assistant_id_fkey', 'assistant_memories', type_='foreignkey')
    op.alter_column('assistant_memories', 'assistant_id', new_column_name='user_id')
    op.rename_table('assistant_memories', 'user_memories')
    op.create_foreign_key('user_memories_user_id_fkey', 'user_memories', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('assistant_capabilities_assistant_id_fkey', 'assistant_capabilities', type_='foreignkey')
    op.alter_column('assistant_capabilities', 'assistant_id', new_column_name='user_id')
    op.rename_table('assistant_capabilities', 'user_capabilities')
    op.create_foreign_key('user_capabilities_user_id_fkey', 'user_capabilities', 'assistants', ['user_id'], ['id'])
    
    # Revert all other foreign key constraints and column renames
    op.drop_constraint('organizations_created_by_fkey', 'organizations', type_='foreignkey')
    op.create_foreign_key('organizations_created_by_fkey', 'organizations', 'assistants', ['created_by'], ['id'])
    
    op.drop_constraint('agent_assignments_assistant_id_fkey', 'agent_assignments', type_='foreignkey')
    op.alter_column('agent_assignments', 'assistant_id', new_column_name='user_id')
    op.create_foreign_key('agent_assignments_user_id_fkey', 'agent_assignments', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('steps_assistant_id_fkey', 'steps', type_='foreignkey')
    op.alter_column('steps', 'assistant_id', new_column_name='user_id')
    op.create_foreign_key('steps_user_id_fkey', 'steps', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('episodes_initiator_id_fkey', 'episodes', type_='foreignkey')
    op.create_foreign_key('episodes_initiator_id_fkey', 'episodes', 'assistants', ['initiator_id'], ['id'])
    
    op.drop_constraint('scenarios_created_by_fkey', 'scenarios', type_='foreignkey')
    op.create_foreign_key('scenarios_created_by_fkey', 'scenarios', 'assistants', ['created_by'], ['id'])
    
    op.drop_constraint('custom_fields_assistant_id_fkey', 'custom_fields', type_='foreignkey')
    op.alter_column('custom_fields', 'assistant_id', new_column_name='user_id')
    op.create_foreign_key('custom_fields_user_id_fkey', 'custom_fields', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('uq_participant_conversation_assistant', 'chat_participants', type_='unique')
    op.drop_constraint('chat_participants_assistant_id_fkey', 'chat_participants', type_='foreignkey')
    op.alter_column('chat_participants', 'assistant_id', new_column_name='user_id')
    op.create_unique_constraint('uq_participant_conversation_user', 'chat_participants', ['conversation_id', 'user_id'])
    op.create_foreign_key('chat_participants_user_id_fkey', 'chat_participants', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('chat_messages_sender_id_fkey', 'chat_messages', type_='foreignkey')
    op.create_foreign_key('chat_messages_sender_id_fkey', 'chat_messages', 'assistants', ['sender_id'], ['id'])
    
    op.drop_constraint('chat_conversations_created_by_fkey', 'chat_conversations', type_='foreignkey')
    op.create_foreign_key('chat_conversations_created_by_fkey', 'chat_conversations', 'assistants', ['created_by'], ['id'])
    
    op.drop_constraint('task_attachments_assistant_id_fkey', 'task_attachments', type_='foreignkey')
    op.alter_column('task_attachments', 'assistant_id', new_column_name='user_id')
    op.create_foreign_key('task_attachments_user_id_fkey', 'task_attachments', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('task_comments_assistant_id_fkey', 'task_comments', type_='foreignkey')
    op.alter_column('task_comments', 'assistant_id', new_column_name='user_id')
    op.create_foreign_key('task_comments_user_id_fkey', 'task_comments', 'assistants', ['user_id'], ['id'])
    
    op.drop_constraint('tasks_assigned_by_fkey', 'tasks', type_='foreignkey')
    op.drop_constraint('tasks_assigned_to_fkey', 'tasks', type_='foreignkey')
    op.drop_constraint('tasks_created_by_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_assigned_by_fkey', 'tasks', 'assistants', ['assigned_by'], ['id'])
    op.create_foreign_key('tasks_assigned_to_fkey', 'tasks', 'assistants', ['assigned_to'], ['id'])
    op.create_foreign_key('tasks_created_by_fkey', 'tasks', 'assistants', ['created_by'], ['id'])
    
    # Revert self-referencing foreign key and table rename
    op.drop_constraint('assistants_created_by_fkey', 'assistants', type_='foreignkey')
    op.create_foreign_key('users_created_by_fkey', 'assistants', 'assistants', ['created_by'], ['id'])
    
    # Finally, rename assistants table back to users
    op.rename_table('assistants', 'users')