"""Ad service."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.models import AdOrm
from ad_service.repositories import AdRepository
from ad_service.schemas import AdCreate, AdRead, AdUpdate, PaginatedAds


class AdService:
    def __init__(self, session: AsyncSession) -> None:
        self.repo = AdRepository(session)

    async def create(self, payload: AdCreate) -> AdRead:
        ad = AdOrm(
            title=payload.title,
            category=payload.category,
            price=payload.price,
            name=payload.name,
            owner_id=payload.owner_id,
        )
        created = await self.repo.create(ad)
        return AdRead.model_validate(created)

    async def get(self, ad_id: int) -> AdRead | None:
        ad = await self.repo.get(ad_id)
        if ad is None:
            return None
        return AdRead.model_validate(ad)

    async def list(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        category: str | None = None,
        owner_id: int | None = None,
    ) -> PaginatedAds:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
        items, total = await self.repo.paginate(
            page=page, page_size=page_size, category=category, owner_id=owner_id
        )
        return PaginatedAds(
            items=[AdRead.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def update(self, ad_id: int, payload: AdUpdate) -> AdRead | None:
        updated = await self.repo.update(
            ad_id, **payload.model_dump(exclude_unset=True)
        )
        if updated is None:
            return None
        return AdRead.model_validate(updated)

    async def delete(self, ad_id: int) -> bool:
        return await self.repo.delete(ad_id)
