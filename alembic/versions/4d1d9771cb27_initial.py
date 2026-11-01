"""initial

Revision ID: 4d1d9771cb27
Revises:
Create Date: 2026-10-28 22:15:55.144241
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4d1d9771cb27"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_name", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password", sa.String(255), nullable=False),
    )
    op.create_table(
        "ads",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ads")
    op.drop_table("users")
