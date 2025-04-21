# Import all the models, so that Base has them before being
# imported by Alembic
from ..db.base_class import Base  # noqa
from ..models.user import User  # noqa
from ..models.task import Task, TaskComment, TaskAttachment  # noqa
from ..models.user_capability import UserCapability  # noqa
from ..models.memory import UserMemory  # noqa
from ..models.verification_code import VerificationCode  # noqa 