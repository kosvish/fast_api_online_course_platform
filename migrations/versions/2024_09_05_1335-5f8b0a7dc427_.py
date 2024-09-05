"""empty message

Revision ID: 5f8b0a7dc427
Revises: fc48ac726355
Create Date: 2024-09-05 13:35:09.989516

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5f8b0a7dc427"
down_revision: Union[str, None] = "fc48ac726355"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.VARCHAR(),
        type_=sa.LargeBinary(),
        existing_nullable=False,
        postgresql_using="hash_password::bytea"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.LargeBinary(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
        postgresql_using="hash_password::varchar"
    )
    # ### end Alembic commands ###
