"""User routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.dependencies import get_db
from ad_service.schemas import UserCreate, UserRead, UserUpdate
from ad_service.services import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate, session: AsyncSession = Depends(get_db)
) -> UserRead:
    service = UserService(session)
    return await service.create(payload)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int, session: AsyncSession = Depends(get_db)
) -> UserRead:
    service = UserService(session)
    user = await service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    session: AsyncSession = Depends(get_db),
) -> UserRead:
    service = UserService(session)
    updated = await service.update(user_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, session: AsyncSession = Depends(get_db)
) -> None:
    service = UserService(session)
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
