from .main import templates
from fastapi import Request, Depends
from app.db.models import CourseModel
from ..api.routes.courses import get_all_courses
from fastapi import APIRouter


router = APIRouter()


@router.get("/all-courses")
async def get_all_courses_route_page(
    request: Request, courses: list[CourseModel] = Depends(get_all_courses)
):
    return templates.TemplateResponse(
        "courses/main.html", context={"request": request, "courses": courses}
    )
