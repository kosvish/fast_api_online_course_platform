from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session


async def get_async_session() -> AsyncSession:
    async with async_session() as conn:
        yield conn
