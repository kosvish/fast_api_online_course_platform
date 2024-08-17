from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import CourseModel, UserModel


def check_user_in_course_participants(
    course_with_participants: CourseModel, user: UserModel
):
    if user not in course_with_participants.participants:
        return True
    else:
        return False
