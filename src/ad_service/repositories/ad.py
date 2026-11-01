"""Ad repository."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.models import AdOrm
from ad_service.repositories.base import BaseRepository


class AdRepository(BaseRepository[AdOrm]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(AdOrm, session)

    async def get_by_category(self, category: str) -> list[AdOrm]:
        result = await self.session.execute(
            select(AdOrm).where(AdOrm.category == category)
        )
        return list(result.scalars().all())

    async def get_by_owner(self, owner_id: int) -> list[AdOrm]:
        result = await self.session.execute(
            select(AdOrm).where(AdOrm.owner_id == owner_id)
        )
        return list(result.scalars().all())

    async def paginate(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        category: str | None = None,
        owner_id: int | None = None,
    ) -> tuple[list[AdOrm], int]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20

        query = select(AdOrm)
        count_query = select(func.count()).select_from(AdOrm)

        if category is not None:
            query = query.where(AdOrm.category == category)
            count_query = count_query.where(AdOrm.category == category)
        if owner_id is not None:
            query = query.where(AdOrm.owner_id == owner_id)
            count_query = count_query.where(AdOrm.owner_id == owner_id)

        skip = (page - 1) * page_size
        result = await self.session.execute(
            query.offset(skip).limit(page_size)
        )
        items = list(result.scalars().all())

        total_result = await self.session.execute(count_query)
        total = int(total_result.scalar_one())

        return items, total
