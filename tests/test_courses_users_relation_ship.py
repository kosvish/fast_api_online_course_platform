from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel, CourseUserAssociation
from app.crud import (
    create_user,
    create_course,
    delete_all_users,
    delete_all_courses,
    select_user_by_id,
)
from app.crud.course_user_relationship import (
    select_course_with_creator_by_id,
    select_course_with_participants_by_id,
    select_all_courses_with_participants,
    add_participants_to_course_by_id,
)
from app.crud.user import select_user_by_id, select_all_users
import pytest


@pytest.fixture
async def create_users_courses(session, courses_data, users_data):
    for user in users_data:
        await create_user(session, **user)
    for course in courses_data:
        await create_course(session, **course)

    yield
    await delete_all_users(session)
    await delete_all_courses(session)


@pytest.mark.usefixtures("create_users_courses")
class TestCourseUserRelation:
    async def test_count_all_courses(self, session, courses_data):
        courses = await select_all_courses_with_participants(session)
        assert len(courses_data) == len(courses)

    async def test_select_course_with_users_by_id(self, session, courses_data):
        course = await select_course_with_creator_by_id(session, 1)
        user = await select_user_by_id(session, 1)
        assert course.creator == user

    async def test_select_course_with_participants_by_id(self, session):
        course_with_participants = await select_course_with_participants_by_id(
            session, 1
        )
        assert len(course_with_participants.participants) == 0

    async def test_add_participants_to_course_by_id(self, session, users_data):
        course = await select_course_with_participants_by_id(session, 1)
        users = await select_all_users(session)
        await add_participants_to_course_by_id(session, course, *users)
        course = await select_course_with_participants_by_id(session, 1)
        assert len(course.participants) == len(users_data)
