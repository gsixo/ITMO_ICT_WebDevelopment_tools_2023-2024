from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import notification as crud
from app.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationRead,
    NotificationUpdate,
    NotificationWithRelations,
)

router = APIRouter()


@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification(
    data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
) -> NotificationRead:
    return await crud.create_notification(db, data)


@router.get("/", response_model=list[NotificationRead])
async def list_notifications(
    person_id: int | None = None,
    is_read: bool | None = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[NotificationRead]:
    return await crud.get_notifications(db, person_id=person_id, is_read=is_read, skip=skip, limit=limit)


@router.get("/{notification_id}", response_model=NotificationWithRelations)
async def get_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
) -> NotificationWithRelations:
    notification = await crud.get_notification_with_relations(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


@router.patch("/{notification_id}", response_model=NotificationRead)
async def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    db: AsyncSession = Depends(get_db),
) -> NotificationRead:
    notification = await crud.update_notification(db, notification_id, data)
    if notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification


@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    deleted = await crud.delete_notification(db, notification_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
