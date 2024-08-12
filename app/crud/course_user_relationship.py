from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import UserModel, CourseModel, CourseUserAssociation
from .course import select_course_by_id
from .user import select_user_by_id


async def select_all_courses_with_users_in_it(
    session: AsyncSession,
) -> list[CourseModel]:
    query = select(CourseModel).options(
        selectinload(CourseModel.users_detail).joinedload(CourseUserAssociation.user)
    )
    result = await session.scalars(query)
    return list(result)


async def add_user_in_course(session: AsyncSession, user_id: int, course_id: int):
    course = await select_course_by_id(session, course_id)
    user = await select_user_by_id(session, user_id)
    course.users_detail.append(CourseUserAssociation(
        user=user
    ))

    await session.commit()

