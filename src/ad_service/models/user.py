"""User model."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ad_service.database import Base


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    ads: Mapped[list["AdOrm"]] = relationship(back_populates="owner")
