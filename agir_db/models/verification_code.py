from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class VerificationCode(Base):
    __tablename__ = "verification_codes"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(index=True, nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    is_used: Mapped[bool] = mapped_column(default=False) 