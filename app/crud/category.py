from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category, CategoryTypeEnum
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get_category(db: AsyncSession, category_id: int) -> Category | None:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_categories(
    db: AsyncSession,
    type_filter: CategoryTypeEnum | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Category]:
    stmt = select(Category).offset(skip).limit(limit)
    if type_filter is not None:
        stmt = stmt.where(Category.type == type_filter)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def update_category(db: AsyncSession, category_id: int, data: CategoryUpdate) -> Category | None:
    category = await get_category(db, category_id)
    if category is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    category = await get_category(db, category_id)
    if category is None:
        return False
    await db.delete(category)
    await db.commit()
    return True
