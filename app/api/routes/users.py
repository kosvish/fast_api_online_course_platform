from typing import Any

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_async_session
from app.crud.user import (
    create_user,
    select_user_by_id,
    select_all_users,
    delete_user_by_id,
)

from app.api.schemas import (
    CreateUser,
    UpdateUser,
    ResponseUser,
    UpdateUserPartial,
    UserSchema,
)
from app.utils import check_unique_user_email
from app.db.models import UserModel
from app.api.dependencies import get_user_by_id as get_user_by_id_dependencies
from app.crud.user import update_user_by_id as update_user_by_id_func
from app.crud.course_user_relationship import select_current_user_with_courses_by_id
from app.api.auth import get_current_token_payload
from app.api.dependencies import get_current_user_by_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_route(
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
        "status": status.HTTP_201_CREATED,
        "detail": {
            "message": "Congratulations! You're successfully registered",
            "user": user_data.model_dump(exclude={"hash_password"}),
        },
    }


@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user_by_id_route(
    user_id: int,
    user_data: UpdateUserPartial,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(get_user_by_id_dependencies),
) -> ResponseUser:
    user = await update_user_by_id_func(
        session, user, **user_data.model_dump(exclude_none=True)
    )

    return ResponseUser(username=user.username, email=user.email)


@router.get("/get/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id_route(
    user_id: int,
    user: UserModel = Depends(get_user_by_id_dependencies),
) -> ResponseUser:
    return ResponseUser(username=user.username, email=user.email)


@router.delete("/delete/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_by_id_route(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    await delete_user_by_id(session, user_id)
    return {
        "status": status.HTTP_200_OK,
        "detail": f"User {user_id} successfully deleted",
    }


@router.get("/get/{user_id}/courses")
async def get_user_by_id_with_courses_route(
    user: UserModel = Depends(get_user_by_id_dependencies),
    session: AsyncSession = Depends(get_async_session),
):
    user = await select_current_user_with_courses_by_id(user, session)
    return {"user_courses": user.enrolled_course}


@router.get("/profile", response_model=ResponseUser)
async def get_user_profile(
    current_user: UserModel = Depends(get_current_user_by_token),
):
    return ResponseUser(username=current_user.username, email=current_user.email)
