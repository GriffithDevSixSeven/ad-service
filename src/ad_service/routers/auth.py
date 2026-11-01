"""Auth routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ad_service.core.security import create_access_token
from ad_service.dependencies import get_db
from ad_service.schemas import Token
from ad_service.services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
) -> Token:
    service = UserService(session)
    user = await service.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)
