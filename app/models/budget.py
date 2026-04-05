from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, SmallInteger, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.notification import Notification
    from app.models.person import Person


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (
        UniqueConstraint("person_id", "category_id", "period_year", "period_month", name="uq_budget_person_cat_period"),
        CheckConstraint("period_month BETWEEN 1 AND 12", name="ck_budget_period_month"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    period_year: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    period_month: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    person: Mapped["Person"] = relationship("Person", back_populates="budgets")
    category: Mapped["Category"] = relationship("Category", back_populates="budgets")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="budget")
