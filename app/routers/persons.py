from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import person as crud
from app.database import get_db
from app.schemas.person import PersonCreate, PersonRead, PersonUpdate, PersonWithAccounts

router = APIRouter()


@router.post("/", response_model=PersonRead, status_code=status.HTTP_201_CREATED)
async def create_person(
    data: PersonCreate,
    db: AsyncSession = Depends(get_db),
) -> PersonRead:
    return await crud.create_person(db, data)


@router.get("/", response_model=list[PersonRead])
async def list_persons(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[PersonRead]:
    return await crud.get_persons(db, skip=skip, limit=limit)


@router.get("/{person_id}", response_model=PersonRead)
async def get_person(
    person_id: int,
    db: AsyncSession = Depends(get_db),
) -> PersonRead:
    person = await crud.get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.get("/{person_id}/full", response_model=PersonWithAccounts)
async def get_person_with_accounts(
    person_id: int,
    db: AsyncSession = Depends(get_db),
) -> PersonWithAccounts:
    person = await crud.get_person_with_accounts(db, person_id)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.patch("/{person_id}", response_model=PersonRead)
async def update_person(
    person_id: int,
    data: PersonUpdate,
    db: AsyncSession = Depends(get_db),
) -> PersonRead:
    person = await crud.update_person(db, person_id, data)
    if person is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_person(
    person_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await crud.delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
