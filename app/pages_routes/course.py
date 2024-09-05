from .main import templates
from fastapi import Request, Depends, status
from app.db.models import CourseModel
from ..api.routes.courses import get_all_courses, get_course_by_id_route
from fastapi import APIRouter


router = APIRouter()


@router.get("/all-courses")
async def get_all_courses_route_page(
    request: Request, courses: list[CourseModel] = Depends(get_all_courses)
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
