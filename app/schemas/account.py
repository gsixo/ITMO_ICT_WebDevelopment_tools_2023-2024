from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.account import AccountTypeEnum
from app.schemas.transaction import TransactionWithCategory


class AccountBase(BaseModel):
    name: str
    type: AccountTypeEnum = AccountTypeEnum.checking
    currency: str = "RUB"
    balance: Decimal = Decimal("0.00")


class AccountCreate(AccountBase):
    person_id: int


class AccountUpdate(BaseModel):
    name: str | None = None
    type: AccountTypeEnum | None = None
    currency: str | None = None
    balance: Decimal | None = None


class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    person_id: int
    created_at: datetime


class AccountWithTransactions(AccountRead):
    transactions: list[TransactionWithCategory] = Field(default_factory=list)
