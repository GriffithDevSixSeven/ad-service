"""Custom exceptions."""

from __future__ import annotations


class AppError(Exception):
    """Base application error."""


class NotFoundError(AppError):
    """Resource not found."""


class ConflictError(AppError):
    """Resource conflict (e.g. duplicate)."""
