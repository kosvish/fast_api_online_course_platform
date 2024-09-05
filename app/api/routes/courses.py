from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import CourseUpdatePartial
from app.api.dependencies import get_async_session
from app.api.schemas import Course, CourseResponse, CourseCreateProd, ResponseUser
from fastapi import status
from app.crud.course import (
    select_all_courses,
    create_course,
    update_course_by_id,
    select_course_by_id,
    delete_course_by_id,
)
from app.db.models import UserModel
from app.api.dependencies import get_current_user_by_token, get_course_by_id
from app.crud.course_user_relationship import (
    select_course_with_participants_by_id,
    select_course_with_creator_by_id,
    select_course_participants_by_course_id,
)
from app.db.models import CourseModel
from app.utils import check_is_owner_user_course, check_user_in_course_participants

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/all")
async def get_all_courses(
    session: AsyncSession = Depends(get_async_session),
) -> list[Course]:
    courses = await select_all_courses(session)
    return courses


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=CourseResponse
)
async def create_courses(
    course_create: CourseCreateProd,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user_by_token),
):
    course = await create_course(
        session,
        title=course_create.title,
        description=course_create.description,
        code_language=course_create.code_language,
        creator_id=current_user.id,
    )
    await session.refresh(course)
    return CourseResponse(
        title=course.title,
        description=course.description,
        code_language=course.code_language,
    )


@router.get("/{course_id}/enroll", status_code=status.HTTP_200_OK)
async def enroll_course(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user_by_token),
    current_course: CourseModel = Depends(get_course_by_id)
) -> dict:

    course = await select_course_with_participants_by_id(session, course_id)
    if check_user_in_course_participants(course, current_user):
        course.participants.append(current_user)
        await session.commit()
        await session.refresh(course)
        return {
            "status": status.HTTP_200_OK,
            "message": f"You successfully joined at course {course.title}!",
        }


@router.put(
    "/{course_id}/update", response_model=CourseResponse, status_code=status.HTTP_200_OK
)
async def update_course_route(
    course_id: int,
    update_course: CourseUpdatePartial,
    session: AsyncSession = Depends(get_async_session),
    current_user: UserModel = Depends(get_current_user_by_token),
):
    try:
        course = await select_course_by_id(session, course_id)
        if check_is_owner_user_course(course, current_user):
            course = await update_course_by_id(
                session, course_id, **update_course.model_dump(exclude_none=True)
            )
            return CourseResponse(
                title=course.title,
                description=course.description,
                code_language=course.code_language,
            )
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with id: {course_id} not found",
        )


@router.get(
    "/{course_id}", response_model=CourseResponse, status_code=status.HTTP_200_OK
)
async def get_course_by_id_route(
    course: CourseModel = Depends(get_course_by_id),
):
    user = ResponseUser(username=course.creator.username, email=course.creator.email)
    return CourseResponse(
        title=course.title,
        description=course.description,
        code_language=course.code_language,
        creator=user,
        price=course.price
    )


@router.delete("/{course_id}/delete", status_code=status.HTTP_200_OK)
async def delete_course_by_id_route(
    course_id: int,
    current_user: UserModel = Depends(get_current_user_by_token),
    session: AsyncSession = Depends(get_async_session),
):
    course = await select_course_by_id(session, course_id)
    if check_is_owner_user_course(course, current_user):
        await delete_course_by_id(session, course_id)
    return {
        "status": status.HTTP_200_OK,
        "message": f"Course {course.title} was successfully deleted!",
    }


# create routes relation between course - user


@router.get(
    "/{course_id}/creator", response_model=ResponseUser, status_code=status.HTTP_200_OK
)
async def get_course_creator_route(
    course_id: int,
    session: AsyncSession = Depends(get_async_session),
    course: CourseModel = Depends(get_course_by_id),
):
    course = await select_course_with_creator_by_id(session, course_id)
    creator: UserModel = course.creator
    return ResponseUser(username=creator.username, email=creator.email)


@router.get("/{course_id}/participants", status_code=status.HTTP_200_OK)
async def get_course_participants_route(
    course_id: int,
    current_user: UserModel = Depends(get_current_user_by_token),
    session: AsyncSession = Depends(get_async_session),
    course: CourseModel = Depends(get_course_by_id),
):
    if course.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have not enough permissions to view this page",
        )
    course_participants = await select_course_participants_by_course_id(course_id, session)
    return [
        ResponseUser(username=participant.username, email=participant.email)
        for participant in course_participants
    ]
