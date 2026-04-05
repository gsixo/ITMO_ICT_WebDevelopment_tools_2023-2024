from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.goal import GoalStatusEnum
from app.schemas.account import AccountRead
from app.schemas.person import PersonRead


class GoalBase(BaseModel):
    name: str
    description: str | None = None
    target_amount: Decimal
    current_amount: Decimal = Decimal("0.00")
    deadline: date | None = None
    status: GoalStatusEnum = GoalStatusEnum.active


class GoalCreate(GoalBase):
    person_id: int
    account_id: int | None = None


class GoalUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    target_amount: Decimal | None = None
    current_amount: Decimal | None = None
    deadline: date | None = None
    status: GoalStatusEnum | None = None
    account_id: int | None = None


class GoalRead(GoalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    person_id: int
    account_id: int | None
    created_at: datetime
    updated_at: datetime


class GoalWithRelations(GoalRead):
    person: PersonRead
    account: AccountRead | None = None
