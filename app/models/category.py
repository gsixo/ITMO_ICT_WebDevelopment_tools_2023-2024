import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.budget import Budget
    from app.models.transaction import Transaction


class CategoryTypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"
    both = "both"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    type: Mapped[CategoryTypeEnum] = mapped_column(
        Enum(CategoryTypeEnum, native_enum=True), nullable=False, default=CategoryTypeEnum.expense
    )
    is_system: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )
    budgets: Mapped[list["Budget"]] = relationship(
        "Budget", back_populates="category", cascade="all, delete-orphan"
    )
