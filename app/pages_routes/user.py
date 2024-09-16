from fastapi import APIRouter, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from .main import templates
from fastapi import Request, Depends
from typing import Annotated

from ..api.auth.routes import validate_auth_user, login_user
from ..api.auth.utils import encode_jwt_token
from ..api.dependencies import get_async_session, get_current_user_by_token
from ..api.routes.users import (
    create_user_route,
    get_user_created_courses_through_profile,
    get_user_enrolled_courses_through_profile,
)
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
        return RedirectResponse(url=request.url_for("user_login_get"), status_code=303)


@router.post("/login")
async def user_login_post(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_async_session),
):
    user = await validate_auth_user(username, password, session)
    if user:
        jwt_payload = {"sub": user.id, "username": user.username, "email": user.email}
        token = encode_jwt_token(jwt_payload)
        response = RedirectResponse(
            url=request.url_for("user_profile_get"), status_code=303
        )
        response.set_cookie(key="access_token", value=token)
        return response


@router.get("/login")
async def user_login_get(request: Request):
    return templates.TemplateResponse("/users/login.html", {"request": request})


@router.get("/logout")
async def get_logout(
    request: Request, current_user: UserModel = Depends(get_current_user_by_token)
):
    response = RedirectResponse(url=request.url_for("get_main_page"))
    response.delete_cookie(key="access_token")
    return response


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


@router.get("/profile/my-created-course")
async def user_profile_created_course_get(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(get_current_user_by_token),
):
    courses = await get_user_created_courses_through_profile(user, session)
    return templates.TemplateResponse(
        "/users/my_created_course.html", {"request": request, "courses": courses}
    )


@router.get("/profile/my-enrolled-course")
async def user_profile_enrolled_course_get(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(get_current_user_by_token),
):
    courses = await get_user_enrolled_courses_through_profile(user, session)
    return templates.TemplateResponse(
        "/users/my_enrolled_course.html", {"request": request, "courses": courses}
    )
