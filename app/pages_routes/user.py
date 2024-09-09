from fastapi import APIRouter, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .main import templates
from fastapi import Request, Depends, status
from typing import Annotated

from ..api.auth.routes import validate_auth_user
from ..api.dependencies import get_async_session, get_current_user_by_token
from ..api.routes.users import create_user_route
from ..api.schemas import CreateUser
from app.db.models import UserModel

router = APIRouter()


@router.get("/registration")
async def user_registration_form_get(request: Request):
    return templates.TemplateResponse("/users/registration.html", {"request": request})


@router.post("/registration")
async def user_registration_post(
    request: Request,
    username: Annotated[str, Form()],
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session),
):
    data_dict = CreateUser(username=username, email=email, hash_password=password)
    response = await create_user_route(user_data=data_dict, session=session)
    if response:
        return templates.TemplateResponse("/main/main.html", {"request": request})


@router.post("/login")
async def user_login_post(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session),
):
    data = await validate_auth_user(username, password, session)
    if data:
        return templates.TemplateResponse("/main/main.html", {"request": request})


@router.get("/login")
async def user_login_get(request: Request):
    return templates.TemplateResponse("/users/login.html", {"request": request})


@router.get("/profile")
async def user_profile_get(
    request: Request,
    user: UserModel = Depends(get_current_user_by_token),
    session: AsyncSession = Depends(get_async_session),
):
    await session.refresh(user, ["enrolled_course", "created_courses"])

    return templates.TemplateResponse(
        "/users/profile.html", {"request": request, "user": user}
    )
