"""User schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    user_name: str
    email: EmailStr

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
