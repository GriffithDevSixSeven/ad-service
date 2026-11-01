"""User repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.models import UserOrm
from ad_service.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserOrm, session)

    async def get_by_user_name(self, user_name: str) -> UserOrm | None:
        result = await self.session.execute(
            select(UserOrm).where(UserOrm.user_name == user_name)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> UserOrm | None:
        result = await self.session.execute(
            select(UserOrm).where(UserOrm.email == email)
        )
        return result.scalar_one_or_none()
