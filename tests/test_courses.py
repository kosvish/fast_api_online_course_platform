from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session_test, async_engine_test, async_engine
from app.db.models import Base, UserModel, CourseModel
from app.crud import (
    create_table,
    drop_table,
    delete_all_courses,
    count_courses,
    create_course,
    create_user,
    delete_all_users,
    select_course_by_id,
    read_user_by_id,
    update_course_by_id,
    delete_course_by_id,
)

import pytest


# title: str,
# description: str,
# code_language: str,
# user_id: int = 1,
@pytest.fixture
def courses():
    courses_data = [
        ["Django", "Best Course for Django", "Python", 1],
        ["FastAPI", "Best Course for FastAPI", "Python", 2],
        ["SQLAlchemy", "Best Course for SQLAlchemy", "Python", 3],
    ]
    return courses_data


@pytest.fixture
def users():
    users_data = [
        ["Test1", "test1@gmail.com", "123"],
        ["Test2", "test2@gmail.com", "123"],
        ["Test3", "test3@gmail.com", "123"],
    ]
    return users_data


@pytest.fixture(scope="function")
async def clear_courses(session):
    await delete_all_courses(session)
    yield


@pytest.fixture(scope="function")
async def create_test_users_for_course(session, users):
    for user in users:
        await create_user(session, *user)
    yield
    await delete_all_users(session)


@pytest.mark.usefixtures("clear_courses")
class TestCrudCourse:
    async def test_create_courses(self, session, courses):
        for course in courses:
            await create_course(session, *course)

        result = await count_courses(session)

        assert result == len(courses)

    async def test_select_course_by_id(self, session, courses):
        title, description, code_language, user_id = courses[0]
        course = await create_course(session, *courses[0])
        fetched_course = await select_course_by_id(session, user_id)
        assert fetched_course.title == title
        assert fetched_course.description == description
        assert fetched_course.code_language == code_language
        assert fetched_course.user_id == user_id

    async def test_update_course_by_id(self, session, courses):
        title, description, code_language, user_id = courses[0]
        course = await create_course(session, *courses[0])
        updated_course = await update_course_by_id(
            session,
            user_id,
            title="UpdatedTitle",
            description="UpdatedDesc",
            code_language="Java",
        )
        assert updated_course.title != title
        assert updated_course.description != description
        assert updated_course.code_language != code_language

    async def test_delete_course_by_id(self, session, courses):
        title, description, code_language, user_id = courses[0]
        course = await create_course(session, *courses[0])
        await delete_course_by_id(session, 1)
        len_result = await count_courses(session)
        assert len_result == 0
