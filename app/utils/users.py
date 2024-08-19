from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserModel
from app.api.dependencies import get_async_session


async def check_unique_user_email(session: AsyncSession, email: str) -> bool:
    query = select(UserModel).where(UserModel.email == email)
    user = await session.scalar(query)
    return True if user is None else False
