from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import goal as crud
from app.database import get_db
from app.models.goal import GoalStatusEnum
from app.schemas.goal import GoalCreate, GoalRead, GoalUpdate, GoalWithRelations

router = APIRouter()


@router.post("/", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
async def create_goal(
    data: GoalCreate,
    db: AsyncSession = Depends(get_db),
) -> GoalRead:
    return await crud.create_goal(db, data)


@router.get("/", response_model=list[GoalRead])
async def list_goals(
    person_id: int | None = None,
    status: GoalStatusEnum | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[GoalRead]:
    return await crud.get_goals(db, person_id=person_id, status=status, skip=skip, limit=limit)


@router.get("/{goal_id}", response_model=GoalWithRelations)
async def get_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
) -> GoalWithRelations:
    goal = await crud.get_goal_with_relations(db, goal_id)
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.patch("/{goal_id}", response_model=GoalRead)
async def update_goal(
    goal_id: int,
    data: GoalUpdate,
    db: AsyncSession = Depends(get_db),
) -> GoalRead:
    goal = await crud.update_goal(db, goal_id, data)
    if goal is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await crud.delete_goal(db, goal_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")
