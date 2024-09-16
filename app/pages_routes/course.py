from sqlalchemy.ext.asyncio import AsyncSession

from .main import templates
from fastapi import Request, Depends, status
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

    response = await enroll_course(course_id, session, user, current_course)
    await session.refresh(user, ["enrolled_course", "created_courses"])
    if response:
        return templates.TemplateResponse(
            "users/profile.html", context={"request": request, "user": user}
        )
