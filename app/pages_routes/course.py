from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .main import templates
from fastapi import Request, Depends, status, HTTPException, Query
from app.db.models import CourseModel
from ..api.dependencies import get_current_user_by_token, get_async_session
from ..api.routes.courses import get_all_courses, get_course_by_id_route, enroll_course
from fastapi import APIRouter
from app.db.models import UserModel, CourseModel


router = APIRouter()


@router.get("/all-courses")
async def get_all_courses_route_page(
    request: Request,
    courses: list[CourseModel] = Depends(get_all_courses),
):
    return templates.TemplateResponse(
        "courses/main.html", context={"request": request, "courses": courses}
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


@router.get("/filter", name="filter_courses")
async def filter_courses(
    request: Request,
    title: str = Query(None),
    price: str = Query(None),
    language: str = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(CourseModel).join(UserModel)

    if title:
        query = query.where(CourseModel.title.itlike(f"%{title}%"))

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
        query = query.where(CourseModel.code_language == language)


    courses = (await session.execute(query)).scalars().all()


    return templates.TemplateResponse(
        "filtered_courses.html", {"request": request, "courses": courses}
    )
