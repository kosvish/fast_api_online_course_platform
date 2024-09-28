import os
import shutil

from fastapi import APIRouter, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from .main import templates
from fastapi import Request, Depends, status
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
from ..api.schemas.users import UpdateUserForm


base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
images_dir = os.path.join(base_dir, "static")
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
            url=request.url_for("user_profile"), status_code=303
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


@router.get("/profile", name="user_profile")
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


@router.get("/profile/update-profile", name="update_profile_form")
async def user_profile_update_form_get(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: UserModel = Depends(get_current_user_by_token),
):
    return templates.TemplateResponse(
        "/users/update_profile.html", {"request": request}
    )


@router.post(
    "/profile/update-profile",
    status_code=status.HTTP_200_OK,
    name="update_profile_post",
)
async def update_user_profile_form(
    request: Request,
    username: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    image: UploadFile = File(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user_by_token),
):
    user_data_dict = {
        "username": username,
        "email": email,
        "password": password,
    }
    for attr, value in user_data_dict.items():
        if value is not None:
            setattr(current_user, attr, value)

    if image:
        img_path = f"/user_images/{image.filename}"
        with open(f"{images_dir}/user_images/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        current_user.image_path = img_path

    await session.refresh(current_user, ["enrolled_course", "created_courses"])
    await session.commit()
    return templates.TemplateResponse(
        "/users/profile.html", context={"request": request, "user": current_user}
    )
