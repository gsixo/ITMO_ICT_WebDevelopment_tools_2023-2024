from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import budget as crud
from app.database import get_db
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate, BudgetWithRelations

router = APIRouter()


@router.post("/", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
async def create_budget(
    data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
) -> BudgetRead:
    budget = await crud.create_budget(db, data)
    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Budget for this person/category/period already exists",
        )
    return budget


@router.get("/", response_model=list[BudgetRead])
async def list_budgets(
    person_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[BudgetRead]:
    return await crud.get_budgets(db, person_id=person_id, year=year, month=month, skip=skip, limit=limit)


@router.get("/{budget_id}", response_model=BudgetWithRelations)
async def get_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
) -> BudgetWithRelations:
    budget = await crud.get_budget_with_relations(db, budget_id)
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.patch("/{budget_id}", response_model=BudgetRead)
async def update_budget(
    budget_id: int,
    data: BudgetUpdate,
    db: AsyncSession = Depends(get_db),
) -> BudgetRead:
    budget = await crud.update_budget(db, budget_id, data)
    if budget is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await crud.delete_budget(db, budget_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
