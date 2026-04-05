from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.account import AccountRead


class PersonBase(BaseModel):
    name: str
    email: EmailStr


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class PersonRead(PersonBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class PersonWithAccounts(PersonRead):
    accounts: list[AccountRead] = Field(default_factory=list)
