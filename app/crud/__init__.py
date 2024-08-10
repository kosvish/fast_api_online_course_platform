from .user import (
    create_user,
    read_user_by_id,
    update_user_by_id,
    delete_user_by_id,
    count_all_users,
    delete_all_users,
)
from .dependencies import create_table, drop_table

from .course import create_course, count_courses, delete_all_courses, select_course_by_id, update_course_by_id, delete_course_by_id