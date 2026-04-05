import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.budget import Budget
    from app.models.goal import Goal
    from app.models.person import Person


class NotificationTypeEnum(str, enum.Enum):
    budget_exceeded = "budget_exceeded"
    budget_warning = "budget_warning"
    goal_reached = "goal_reached"
    goal_reminder = "goal_reminder"


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[NotificationTypeEnum] = mapped_column(
        Enum(NotificationTypeEnum, native_enum=True), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    budget_id: Mapped[int | None] = mapped_column(ForeignKey("budgets.id", ondelete="SET NULL"), nullable=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goals.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    person: Mapped["Person"] = relationship("Person", back_populates="notifications")
    budget: Mapped["Budget | None"] = relationship("Budget", back_populates="notifications")
    goal: Mapped["Goal | None"] = relationship("Goal", back_populates="notifications")
