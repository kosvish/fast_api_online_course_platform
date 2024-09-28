import os
import shutil
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from .main import templates
from fastapi import (
    Request,
    Depends,
    status,
    HTTPException,
    Query,
    Form,
    File,
    UploadFile,
)
from ..api.dependencies import get_current_user_by_token, get_async_session
from ..api.routes.courses import get_all_courses, get_course_by_id_route, enroll_course
from fastapi import APIRouter
from app.db.models import UserModel, CourseModel

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
images_dir = os.path.join(base_dir, "static")


@router.get("/all-courses")
async def get_all_courses_route_page(
    request: Request,
    courses: list[CourseModel] = Depends(get_all_courses),
):
    return templates.TemplateResponse(
        "courses/main.html", context={"request": request, "courses": courses}
    )


@router.post("/create", name="create_course_form")
async def create_course_through_form(
    request: Request,
    title: str = Form(),
    description: str = Form(None),
    code_language: str = Form(),
    price: int = Form(None),
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user_by_token),
    image: UploadFile = File(None),
):
    img_path = None
    if image:
        img_path = f"/course_images/{image.filename}"
        with open(f"{images_dir}/course_images/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    query = select(CourseModel).where(CourseModel.title == title)
    exist_course = await session.scalar(query)
    if exist_course is not None:
        raise HTTPException(
            detail="Course with that title already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    new_course = CourseModel(
        title=title,
        description=description,
        code_language=code_language,
        price=price,
        image_path=img_path,
        creator_id=current_user.id,
    )
    session.add(new_course)
    username = current_user.username
    await session.commit()
    current_user = await session.scalar(
        select(UserModel).where(UserModel.username == username)
    )
    await session.refresh(current_user, ["enrolled_course", "created_courses"])
    return templates.TemplateResponse(
        "/users/profile.html", {"request": request, "user": current_user}
    )


@router.get("/create-form", name="get_create_form")
async def get_course_form(
    request: Request, current_user: UserModel = Depends(get_current_user_by_token)
):
    return templates.TemplateResponse(
        "/courses/create_form.html", context={"request": request}
    )


@router.get("/filter", name="filter_courses")
async def filter_courses(
    request: Request,
    title: str = Query(None),
    price: str = Query(None),
    language: str = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(CourseModel)

    if title:
        query = query.where(CourseModel.title.like(f"%{title}%"))

    if price:
        if price == "0-50":
            query = query.where(CourseModel.price < 50)
        elif price == "50-100":
            query = query.where(CourseModel.price.between(50, 100))
        elif price == "100-200":
            query = query.where(CourseModel.price.between(100, 200))
        elif price == "200+":
            query = query.where(CourseModel.price > 200)

    if language:
        query = query.where(CourseModel.code_language == language.title())
    query = query.options(joinedload(CourseModel.creator))
    print(query)
    courses = (await session.execute(query)).scalars().all()

    return templates.TemplateResponse(
        "courses/main.html", {"request": request, "courses": courses}
    )


@router.get("/{course_id}", status_code=status.HTTP_200_OK)
async def get_courses_by_id(
    request: Request,
    course_id: int,
    course: CourseModel = Depends(get_course_by_id_route),
):
    return templates.TemplateResponse(
        "courses/current_course.html", context={"request": request, "course": course}
    )


@router.get("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def get_enroll_course_route(
    request: Request,
    course_id: int,
    user: UserModel = Depends(get_current_user_by_token),
    session: AsyncSession = Depends(get_async_session),
    current_course: CourseModel = Depends(get_course_by_id_route),
):
    try:
        response = await enroll_course(course_id, session, user, current_course)
        await session.refresh(user, ["enrolled_course", "created_courses"])
        if response:
            return templates.TemplateResponse(
                "users/profile.html", context={"request": request, "user": user}
            )
    except HTTPException as exc:
        return templates.TemplateResponse(
            "errors/base.html", context={"request": request, "error_detail": exc.detail}
        )
