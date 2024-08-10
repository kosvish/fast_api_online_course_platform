from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_async_session
from app.db.models import CourseModel, UserModel, CourseUserAssociation
from app.db import async_session
import asyncio


# Создание курса
async def create_course(
    session: AsyncSession,
    title: str,
    description: str,
    code_language: str,
    user_id: int = 1,
) -> CourseModel:
    course = CourseModel(
        title=title,
        description=description,
        code_language=code_language,
        user_id=user_id,
    )

    session.add(course)
    await session.commit()
    return course


async def count_courses(session: AsyncSession) -> int:
    query = select(CourseModel)
    result = await session.scalars(query)
    return len(list(result))


async def select_all_courses(session: AsyncSession) -> list[CourseModel]:
    query = select(CourseModel).order_by(CourseModel.id)
    result = await session.scalars(query)
    return list(result)


async def delete_all_courses(session: AsyncSession) -> None:
    stmt = delete(CourseModel)
    await session.execute(stmt)
    await session.commit()


async def select_course_by_id(
    session: AsyncSession, course_id: int
) -> CourseModel | None:
    query = select(CourseModel).where(CourseModel.id == course_id)
    course = await session.scalar(query)
    return course


async def update_course_by_id(
    session: AsyncSession,
    course_id: int,
    **kwargs,
) -> CourseModel | None:
    query = select(CourseModel).where(CourseModel.id == course_id)
    course = await session.scalar(query)
    for key, value in kwargs.items():
        setattr(course, key, value)

    await session.commit()
    await session.refresh(course)
    return course


async def delete_course_by_id(session: AsyncSession, course_id: int):
    stmt = delete(CourseModel).where(CourseModel.id == course_id)
    await session.execute(stmt)
    await session.commit()
