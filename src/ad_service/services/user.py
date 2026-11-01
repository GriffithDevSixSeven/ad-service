"""User service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.core.security import hash_password, verify_password
from ad_service.models import UserOrm
from ad_service.repositories import UserRepository
from ad_service.schemas import UserCreate, UserRead, UserUpdate


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = UserRepository(session)

    async def create(self, payload: UserCreate) -> UserRead:
        user = UserOrm(
            user_name=payload.user_name,
            email=payload.email,
            password=hash_password(payload.password),
        )
        created = await self.repo.create(user)
        return UserRead.model_validate(created)

    async def get(self, user_id: int) -> UserRead | None:
        user = await self.repo.get(user_id)
        if user is None:
            return None
        return UserRead.model_validate(user)

    async def authenticate(self, user_name: str, password: str) -> UserRead | None:
        user = await self.repo.get_by_user_name(user_name)
        if user is None or not verify_password(password, user.password):
            return None
        return UserRead.model_validate(user)

    async def update(self, user_id: int, payload: UserUpdate) -> UserRead | None:
        data = payload.model_dump(exclude_unset=True)
        if "password" in data and data["password"] is not None:
            data["password"] = hash_password(data["password"])
        updated = await self.repo.update(user_id, **data)
        if updated is None:
            return None
        return UserRead.model_validate(updated)

    async def delete(self, user_id: int) -> bool:
        return await self.repo.delete(user_id)
