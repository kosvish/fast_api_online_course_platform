"""empty message

Revision ID: fc48ac726355
Revises: 504eba719d7f
Create Date: 2024-09-05 13:28:27.890397

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fc48ac726355"
down_revision: Union[str, None] = "504eba719d7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "course_user_association_user_id_fkey",
        "course_user_association",
        type_="foreignkey",
    )
    op.drop_constraint(
        "course_user_association_course_id_fkey",
        "course_user_association",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "course_user_association", "courses", ["course_id"], ["id"]
    )
    op.create_foreign_key(
        None, "course_user_association", "users", ["user_id"], ["id"]
    )
    op.add_column(
        "courses",
        sa.Column("price", sa.Integer(), server_default="500", nullable=False),
    )
    op.drop_constraint("courses_creator_id_key", "courses", type_="unique")
    op.drop_constraint("profiles_user_id_fkey", "profiles", type_="foreignkey")
    op.create_foreign_key(None, "profiles", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "profiles", type_="foreignkey")
    op.create_foreign_key(
        "profiles_user_id_fkey",
        "profiles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_unique_constraint(
        "courses_creator_id_key", "courses", ["creator_id"]
    )
    op.drop_column("courses", "price")
    op.drop_constraint(None, "course_user_association", type_="foreignkey")
    op.drop_constraint(None, "course_user_association", type_="foreignkey")
    op.create_foreign_key(
        "course_user_association_course_id_fkey",
        "course_user_association",
        "courses",
        ["course_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        "course_user_association_user_id_fkey",
        "course_user_association",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###
