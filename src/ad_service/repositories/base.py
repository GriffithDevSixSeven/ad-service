"""Base repository with common CRUD operations."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic asynchronous repository for a SQLAlchemy model."""

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get(self, obj_id: int) -> ModelType | None:
        return await self.session.get(self.model, obj_id)

    async def get_all(self, *, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await self.session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return int(result.scalar_one())

    async def paginate(
        self, *, page: int = 1, page_size: int = 20
    ) -> tuple[list[ModelType], int]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        skip = (page - 1) * page_size
        items = await self.get_all(skip=skip, limit=page_size)
        total = await self.count()
        return items, total

    async def update(self, obj_id: int, **kwargs: Any) -> ModelType | None:
        obj = await self.get(obj_id)
        if obj is None:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get(obj_id)
        if obj is None:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
