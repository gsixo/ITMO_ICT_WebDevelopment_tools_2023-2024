from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.transaction import TransactionTypeEnum
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    store: str
    amount: Decimal
    type: TransactionTypeEnum = TransactionTypeEnum.expense
    transaction_date: date
    description: str | None = None


class TransactionCreate(TransactionBase):
    account_id: int
    category_id: int


class TransactionUpdate(BaseModel):
    store: str | None = None
    amount: Decimal | None = None
    type: TransactionTypeEnum | None = None
    transaction_date: date | None = None
    description: str | None = None
    category_id: int | None = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    category_id: int
    created_at: datetime


class TransactionWithCategory(TransactionRead):
    category: CategoryRead


class TransactionWithRelations(TransactionRead):
    category: CategoryRead
    account: dict[str, object]
