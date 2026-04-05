from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import account as crud
from app.database import get_db
from app.schemas.account import AccountCreate, AccountRead, AccountUpdate, AccountWithTransactions

router = APIRouter()


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(
    data: AccountCreate,
    db: AsyncSession = Depends(get_db),
) -> AccountRead:
    return await crud.create_account(db, data)


@router.get("/", response_model=list[AccountRead])
async def list_accounts(
    person_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[AccountRead]:
    return await crud.get_accounts(db, person_id=person_id, skip=skip, limit=limit)


@router.get("/{account_id}", response_model=AccountRead)
async def get_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
) -> AccountRead:
    account = await crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.get("/{account_id}/full", response_model=AccountWithTransactions)
async def get_account_with_transactions(
    account_id: int,
    db: AsyncSession = Depends(get_db),
) -> AccountWithTransactions:
    account = await crud.get_account_with_transactions(db, account_id)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.patch("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: int,
    data: AccountUpdate,
    db: AsyncSession = Depends(get_db),
) -> AccountRead:
    account = await crud.update_account(db, account_id, data)
    if account is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await crud.delete_account(db, account_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
