"""Ad routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.dependencies import get_db
from ad_service.schemas import AdCreate, AdRead, AdUpdate, PaginatedAds
from ad_service.services import AdService

router = APIRouter(prefix="/ads", tags=["ads"])


@router.post("", response_model=AdRead, status_code=status.HTTP_201_CREATED)
async def create_ad(
    payload: AdCreate, session: AsyncSession = Depends(get_db)
) -> AdRead:
    service = AdService(session)
    return await service.create(payload)


@router.get("", response_model=PaginatedAds)
async def list_ads(
    page: int = 1,
    page_size: int = 20,
    category: str | None = None,
    owner_id: int | None = None,
    session: AsyncSession = Depends(get_db),
) -> PaginatedAds:
    service = AdService(session)
    return await service.list(
        page=page, page_size=page_size, category=category, owner_id=owner_id
    )


@router.get("/{ad_id}", response_model=AdRead)
async def get_ad(
    ad_id: int, session: AsyncSession = Depends(get_db)
) -> AdRead:
    service = AdService(session)
    ad = await service.get(ad_id)
    if ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad


@router.patch("/{ad_id}", response_model=AdRead)
async def update_ad(
    ad_id: int,
    payload: AdUpdate,
    session: AsyncSession = Depends(get_db),
) -> AdRead:
    service = AdService(session)
    updated = await service.update(ad_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return updated


@router.delete("/{ad_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ad(
    ad_id: int, session: AsyncSession = Depends(get_db)
) -> None:
    service = AdService(session)
    deleted = await service.delete(ad_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ad not found")
