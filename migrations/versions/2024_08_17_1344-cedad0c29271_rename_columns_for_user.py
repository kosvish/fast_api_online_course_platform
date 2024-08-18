"""rename columns for user

Revision ID: cedad0c29271
Revises: 504eba719d7f
Create Date: 2024-08-17 13:44:14.928300

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cedad0c29271"
down_revision: Union[str, None] = "504eba719d7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создаем временную таблицу с нужными полями
    op.create_table(
        "courses_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("code_language", sa.String(50), nullable=False),
        sa.Column("description", sa.String(250), nullable=False),
        sa.Column("creator_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
    )

    # Удаляем старую таблицу
    op.drop_table("courses")

    # Переименовываем новую таблицу в старое имя
    op.rename_table("courses_temp", "courses")


def downgrade():
    # Восстанавливаем обратные изменения
    op.create_table(
        "courses_temp",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.String(250), nullable=False),
        sa.Column("code_language", sa.String(50), nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # Удаляем новую таблицу
    op.drop_table("courses")

    # Переименовываем временную таблицу обратно
    op.rename_table("courses_temp", "courses")
