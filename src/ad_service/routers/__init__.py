"""Routers package."""

from ad_service.routers.ads import router as ads_router
from ad_service.routers.auth import router as auth_router
from ad_service.routers.users import router as users_router

__all__ = ["ads_router", "auth_router", "users_router"]
