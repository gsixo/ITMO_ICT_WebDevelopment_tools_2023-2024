from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.notification import NotificationTypeEnum
from app.schemas.budget import BudgetRead
from app.schemas.goal import GoalRead
from app.schemas.person import PersonRead


class NotificationBase(BaseModel):
    type: NotificationTypeEnum
    title: str
    message: str
    is_read: bool = False


class NotificationCreate(NotificationBase):
    person_id: int
    budget_id: int | None = None
    goal_id: int | None = None


class NotificationUpdate(BaseModel):
    is_read: bool | None = None


class NotificationRead(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    person_id: int
    budget_id: int | None
    goal_id: int | None
    created_at: datetime


class NotificationWithRelations(NotificationRead):
    person: PersonRead
    budget: BudgetRead | None = None
    goal: GoalRead | None = None
