from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import select_user_by_id
from app.db.models import UserModel
from fastapi import HTTPException, status
from fastapi import Depends
from .db import get_async_session


async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = await select_user_by_id(session, user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sorry, user with id: {user_id} is not found",
        )
