# Import all the models, so that Base has them before being
# imported by Alembic
from agir_db.db.base_class import Base  # noqa
from agir_db.models.user import User  # noqa
from agir_db.models.task import Task, TaskComment, TaskAttachment  # noqa
from agir_db.models.user_capability import UserCapability  # noqa
from agir_db.models.memory import UserMemory  # noqa
from agir_db.models.scenario import Scenario, State, StateTransition  # noqa
from agir_db.models.episode import Episode  # noqa
from agir_db.models.step import Step  # noqa
from agir_db.models.agent_role import AgentRole  # noqa
from agir_db.models.custom_field import CustomField  # noqa
from agir_db.models.agent_assignment import AgentAssignment  # noqa
from agir_db.models.chat_conversation import ChatConversation  # noqa
from agir_db.models.chat_message import ChatMessage, MessageStatus  # noqa
from agir_db.models.chat_participant import ChatParticipant  # noqa
