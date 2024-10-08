"""add image field, price_can be null

Revision ID: ceb02ef8b365
Revises: 5f8b0a7dc427
Create Date: 2024-09-19 20:51:20.962792

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ceb02ef8b365"
down_revision: Union[str, None] = "5f8b0a7dc427"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "courses",
        sa.Column(
            "image_path",
            sa.String(),
            server_default='/courses-1.jpg',
            nullable=True,
        ),
    )
    op.alter_column(
        "courses",
        "price",
        existing_type=sa.INTEGER(),
        nullable=True,
        existing_server_default=sa.text("500"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "courses",
        "price",
        existing_type=sa.INTEGER(),
        nullable=False,
        existing_server_default=sa.text("500"),
    )
    op.drop_column("courses", "image_path")
    # ### end Alembic commands ###
