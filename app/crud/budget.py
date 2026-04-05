from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


async def get_budget(db: AsyncSession, budget_id: int) -> Budget | None:
    result = await db.execute(select(Budget).where(Budget.id == budget_id))
    return result.scalar_one_or_none()


async def get_budgets(
    db: AsyncSession,
    person_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Budget]:
    stmt = select(Budget).offset(skip).limit(limit)
    if person_id is not None:
        stmt = stmt.where(Budget.person_id == person_id)
    if year is not None:
        stmt = stmt.where(Budget.period_year == year)
    if month is not None:
        stmt = stmt.where(Budget.period_month == month)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_budget_with_relations(db: AsyncSession, budget_id: int) -> Budget | None:
    result = await db.execute(
        select(Budget)
        .options(
            selectinload(Budget.person),
            selectinload(Budget.category),
        )
        .where(Budget.id == budget_id)
    )
    return result.scalar_one_or_none()


async def create_budget(db: AsyncSession, data: BudgetCreate) -> Budget | None:
    budget = Budget(**data.model_dump())
    db.add(budget)
    try:
        await db.commit()
        await db.refresh(budget)
        return budget
    except IntegrityError:
        await db.rollback()
        return None


async def update_budget(db: AsyncSession, budget_id: int, data: BudgetUpdate) -> Budget | None:
    budget = await get_budget(db, budget_id)
    if budget is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(budget, field, value)
    await db.commit()
    await db.refresh(budget)
    return budget


async def delete_budget(db: AsyncSession, budget_id: int) -> bool:
    budget = await get_budget(db, budget_id)
    if budget is None:
        return False
    await db.delete(budget)
    await db.commit()
    return True
