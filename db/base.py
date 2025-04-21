# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.task import Task, TaskComment, TaskAttachment  # noqa
from app.models.user_capability import UserCapability  # noqa
from app.models.memory import UserMemory  # noqa
from app.models.verification_code import VerificationCode  # noqa 