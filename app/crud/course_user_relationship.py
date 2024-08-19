from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserModel, CourseModel, CourseUserAssociation
from .course import select_course_by_id
from .user import select_user_by_id
from app.utils import check_user_in_course_participants


async def select_all_courses_with_participants(
    session: AsyncSession,
) -> list[CourseModel]:
    query = (
        select(CourseModel)
        .options(selectinload(CourseModel.participants))
        .order_by(CourseModel.id)
    )

    courses = await session.scalars(query)

    return list(courses)


async def select_course_with_participants_by_id(
    session: AsyncSession, course_id: int
) -> CourseModel | None:
    query = (
        select(CourseModel)
        .where(CourseModel.id == course_id)
        .options(selectinload(CourseModel.participants))
        .order_by(CourseModel.id)
    )

    course = await session.scalar(query)
    return course


async def select_course_with_creator_by_id(
    session: AsyncSession, course_id: int
) -> CourseModel | None:
    query = (
        select(CourseModel)
        .where(CourseModel.id == course_id)
        .options(joinedload(CourseModel.creator))
    )
    course = await session.scalar(query)
    return course


async def add_participants_to_course(
    session: AsyncSession, course: CourseModel, *participants: UserModel
):
    for user in participants:
        course.participants.append(user)

    await session.commit()


async def delete_user_from_participants_in_course(
    session: AsyncSession, user: UserModel, course_with_participants: CourseModel
):
    course_with_participants.participants.remove(user)
    await session.commit()


async def delete_all_association(session: AsyncSession):
    stmt = delete(CourseUserAssociation)
    await session.execute(stmt)
    await session.commit()
