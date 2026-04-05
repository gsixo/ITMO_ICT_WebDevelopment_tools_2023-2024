from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.notification import Notification
from app.schemas.notification import NotificationCreate, NotificationUpdate


async def get_notification(db: AsyncSession, notification_id: int) -> Notification | None:
    result = await db.execute(select(Notification).where(Notification.id == notification_id))
    return result.scalar_one_or_none()


async def get_notifications(
    db: AsyncSession,
    person_id: int | None = None,
    is_read: bool | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Notification]:
    stmt = select(Notification).offset(skip).limit(limit)
    if person_id is not None:
        stmt = stmt.where(Notification.person_id == person_id)
    if is_read is not None:
        stmt = stmt.where(Notification.is_read == is_read)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_notification_with_relations(db: AsyncSession, notification_id: int) -> Notification | None:
    result = await db.execute(
        select(Notification)
        .options(
            selectinload(Notification.person),
            selectinload(Notification.budget),
            selectinload(Notification.goal),
        )
        .where(Notification.id == notification_id)
    )
    return result.scalar_one_or_none()


async def create_notification(db: AsyncSession, data: NotificationCreate) -> Notification:
    notification = Notification(**data.model_dump())
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def update_notification(
    db: AsyncSession, notification_id: int, data: NotificationUpdate
) -> Notification | None:
    notification = await get_notification(db, notification_id)
    if notification is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(notification, field, value)
    await db.commit()
    await db.refresh(notification)
    return notification


async def delete_notification(db: AsyncSession, notification_id: int) -> bool:
    notification = await get_notification(db, notification_id)
    if notification is None:
        return False
    await db.delete(notification)
    await db.commit()
    return True
