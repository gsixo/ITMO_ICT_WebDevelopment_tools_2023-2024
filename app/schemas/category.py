from pydantic import BaseModel, ConfigDict

from app.models.category import CategoryTypeEnum


class CategoryBase(BaseModel):
    name: str
    icon: str | None = None
    color: str | None = None
    type: CategoryTypeEnum = CategoryTypeEnum.expense


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    icon: str | None = None
    color: str | None = None
    type: CategoryTypeEnum | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_system: bool
