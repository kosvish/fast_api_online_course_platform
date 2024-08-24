from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import CourseModel
from app.api.dependencies import get_async_session, get_course_by_id
from app.api.schemas import (
    CourseCreate,
    Course,
    CourseUpdate,
    CourseUpdatePartial,
)
from fastapi import status
from app.crud.course import select_all_courses, create_course

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/all")
async def get_all_courses(
    session: AsyncSession = Depends(get_async_session),
) -> list[Course]:
    courses = await select_all_courses(session)
    return courses


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_courses(
    course: CourseCreate, session: AsyncSession = Depends(get_async_session)
) -> dict:
    new_course = await create_course(session, )


#
#
# @router.get("/{course_id}", status_code=status.HTTP_200_OK)
# async def get_course(
#     course: CourseModel = Depends(get_course_by_id),
# ):
#     return course
#
#
# @router.put("/update/{course_id}", status_code=status.HTTP_200_OK)
# async def update_course(
#     course_scheme: CourseUpdate,
#     session: AsyncSession = Depends(get_async_session),
#     course: CourseModel = Depends(get_course_by_id),
# ) -> dict:
#
#     for name, value in course_scheme.model_dump().items():
#         setattr(course, name, value)
#     session.add(course)
#     await session.commit()
#
#     await session.refresh(course)
#
#     return {
#         "message": "Successfully updated course",
#         "course": {
#             "title": course.title,
#             "description": course.description,
#             "code_language": course.code_language,
#             "mentor": course.mentor,
#         },
#         "status": status.HTTP_200_OK,
#     }
#
#
# @router.patch("/update/{course_id}", status_code=status.HTTP_200_OK)
# async def update_course_partial(
#     course_scheme: CourseUpdatePartial,
#     session: AsyncSession = Depends(get_async_session),
#     course: CourseModel = Depends(get_course_by_id),
# ) -> dict:
#
#     for name, value in course_scheme.model_dump(exclude_unset=True).items():
#         setattr(course, name, value)
#     session.add(course)
#     await session.commit()
#
#     await session.refresh(course)
#
#     return {
#         "message": "Successfully updated course",
#         "course": {
#             "title": course.title,
#             "description": course.description,
#             "code_language": course.code_language,
#             "mentor": course.mentor,
#         },
#         "status": status.HTTP_200_OK,
#     }
#
#
# @router.delete("/delete/{course_id}", status_code=status.HTTP_200_OK)
# async def delete_course(
#     session: AsyncSession = Depends(get_async_session),
#     course: CourseModel = Depends(get_course_by_id),
# ) -> dict:
#     await session.delete(course)
#     await session.commit()
#     return {
#         "message": "Successfully deleted course",
#         "status": status.HTTP_200_OK,
#     }
