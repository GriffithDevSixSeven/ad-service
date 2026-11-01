"""Ad schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AdCreate(BaseModel):
    title: str
    category: str
    price: float
    name: str
    owner_id: int


class AdRead(BaseModel):
    id: int
    title: str
    category: str
    price: float
    created_at: datetime
    name: str
    owner_id: int

    model_config = {"from_attributes": True}


class AdUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    price: float | None = None
    name: str | None = None
    owner_id: int | None = None


class PaginatedAds(BaseModel):
    items: list[AdRead]
    total: int
    page: int
    page_size: int
