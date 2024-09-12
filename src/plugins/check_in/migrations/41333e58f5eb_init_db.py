"""init db

修订 ID: 41333e58f5eb
父修订:
创建时间: 2023-10-29 11:27:58.965278

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "41333e58f5eb"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = ("check_in",)
depends_on: str | Sequence[str] | None = None


def upgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "check_in_bodyfatrecord",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("body_fat", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_in_bodyfatrecord")),
        info={"bind_key": "check_in"},
    )
    op.create_table(
        "check_in_dietaryrecord",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("healthy", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_in_dietaryrecord")),
        info={"bind_key": "check_in"},
    )
    op.create_table(
        "check_in_fitnessrecord",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_in_fitnessrecord")),
        info={"bind_key": "check_in"},
    )
    op.create_table(
        "check_in_userinfo",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("target_weight", sa.Float(), nullable=True),
        sa.Column("target_body_fat", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_in_userinfo")),
        info={"bind_key": "check_in"},
    )
    op.create_table(
        "check_in_weightrecord",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("time", sa.DateTime(), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_check_in_weightrecord")),
        info={"bind_key": "check_in"},
    )
    # ### end Alembic commands ###


def downgrade(name: str = "") -> None:
    if name:
        return
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("check_in_weightrecord")
    op.drop_table("check_in_userinfo")
    op.drop_table("check_in_fitnessrecord")
    op.drop_table("check_in_dietaryrecord")
    op.drop_table("check_in_bodyfatrecord")
    # ### end Alembic commands ###
