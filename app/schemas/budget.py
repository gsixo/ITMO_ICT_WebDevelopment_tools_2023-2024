from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.category import CategoryRead
from app.schemas.person import PersonRead


class BudgetBase(BaseModel):
    amount: Decimal
    period_year: int
    period_month: int

    @field_validator("period_month")
    @classmethod
    def validate_month(cls, v: int) -> int:
        if not 1 <= v <= 12:
            raise ValueError("period_month must be between 1 and 12")
        return v


class BudgetCreate(BudgetBase):
    person_id: int
    category_id: int


class BudgetUpdate(BaseModel):
    amount: Decimal | None = None


class BudgetRead(BudgetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    person_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime


class BudgetWithRelations(BudgetRead):
    person: PersonRead
    category: CategoryRead
