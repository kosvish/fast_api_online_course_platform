from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_async_session
from app.crud.user import (
    create_user,
    select_user_by_id,
    select_all_users,
    delete_user_by_id,
    update_user_by_id,
)

from app.api.schemas import CreateUser, UpdateUser
from app.utils import check_unique_user_email


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_router(
    user_data: CreateUser, session: AsyncSession = Depends(get_async_session)
) -> dict:
    if await check_unique_user_email(session, user_data.email):
        user = await create_user(session, **user_data.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sorry, email: {user_data.email} is already taken, please if you already registered, sign in",
        )

    return {
        'status': status.HTTP_201_CREATED,
        'detail': {
            'message': "Congratulations! You're succesfully registered",
            'user': user_data.model_dump(exclude={'hash_password'})
        }
    }


