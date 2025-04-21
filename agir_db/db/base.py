# Import all the models, so that Base has them before being
# imported by Alembic
from agir_db.db.base_class import Base  # noqa
from agir_db.models.user import User  # noqa
from agir_db.models.task import Task, TaskComment, TaskAttachment  # noqa
from agir_db.models.user_capability import UserCapability  # noqa
from agir_db.models.memory import UserMemory  # noqa
from agir_db.models.verification_code import VerificationCode  # noqa 