# Import all the models, so that Base has them before being
# imported by Alembic
from agir_db.db.base_class import Base  # noqa
from agir_db.models.assistant import Assistant  # noqa
from agir_db.models.task import Task, TaskComment, TaskAttachment  # noqa
from agir_db.models.assistant_capability import AssistantCapability  # noqa
from agir_db.models.memory import AssistantMemory  # noqa
from agir_db.models.scenario import Scenario  # noqa
from agir_db.models.organization import Organization  # noqa
from agir_db.models.assistant_organization import AssistantOrganization  # noqa
from agir_db.models.state import State  # noqa
from agir_db.models.state_role import StateRole  # noqa
from agir_db.models.state_transition import StateTransition  # noqa
from agir_db.models.episode import Episode  # noqa
from agir_db.models.step import Step  # noqa
from agir_db.models.assistant_role import AssistantRole  # noqa
from agir_db.models.custom_field import CustomField  # noqa
from agir_db.models.assistant_assignment import AssistantAssignment  # noqa
from agir_db.models.chat_conversation import ChatConversation  # noqa
from agir_db.models.chat_message import ChatMessage, MessageStatus  # noqa
from agir_db.models.chat_participant import ChatParticipant  # noqa
