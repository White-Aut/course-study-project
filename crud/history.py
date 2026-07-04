from datetime import datetime

from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News


async def add_history(
    db: AsyncSession,
    user_id: int,
    news_id: int,
):
    stmt = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        existing.viewed_time = datetime.now()
        await db.commit()
        await db.refresh(existing)
        return existing

    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history



async def get_history_list(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 10,
):
    count_query = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()
    offset = (page - 1) * page_size
    query = (
        select(News, History.viewed_time.label("viewed_time"), History.id.label("history_id"))
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.viewed_time.desc())
        .offset(offset).limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total



async def remove_history(
    db: AsyncSession,
    user_id: int,
    history_id: int,
):
    stmt = delete(History).where(History.id == history_id, History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0



async def clear_all_history(
    db: AsyncSession,
    user_id: int,
):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0