from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import select_user_by_id

from app.db.models import UserModel
from fastapi import HTTPException, status
from fastapi import Depends
from .db import get_async_session
from ..auth.routes import get_current_token_payload


async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    user = await select_user_by_id(session, user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sorry, user with id: {user_id} is not found",
        )


async def get_current_user_by_token(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    user_id = payload.get("sub")
    user = await select_user_by_id(session, user_id)
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sorry, user with id: {user_id} is not found",
        )
