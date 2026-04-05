from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.goal import Goal, GoalStatusEnum
from app.schemas.goal import GoalCreate, GoalUpdate


async def get_goal(db: AsyncSession, goal_id: int) -> Goal | None:
    result = await db.execute(select(Goal).where(Goal.id == goal_id))
    return result.scalar_one_or_none()


async def get_goals(
    db: AsyncSession,
    person_id: int | None = None,
    status: GoalStatusEnum | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Goal]:
    stmt = select(Goal).offset(skip).limit(limit)
    if person_id is not None:
        stmt = stmt.where(Goal.person_id == person_id)
    if status is not None:
        stmt = stmt.where(Goal.status == status)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_goal_with_relations(db: AsyncSession, goal_id: int) -> Goal | None:
    result = await db.execute(
        select(Goal)
        .options(
            selectinload(Goal.person),
            selectinload(Goal.account),
        )
        .where(Goal.id == goal_id)
    )
    return result.scalar_one_or_none()


async def create_goal(db: AsyncSession, data: GoalCreate) -> Goal:
    goal = Goal(**data.model_dump())
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


async def update_goal(db: AsyncSession, goal_id: int, data: GoalUpdate) -> Goal | None:
    goal = await get_goal(db, goal_id)
    if goal is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(goal, field, value)
    await db.commit()
    await db.refresh(goal)
    return goal


async def delete_goal(db: AsyncSession, goal_id: int) -> bool:
    goal = await get_goal(db, goal_id)
    if goal is None:
        return False
    await db.delete(goal)
    await db.commit()
    return True
