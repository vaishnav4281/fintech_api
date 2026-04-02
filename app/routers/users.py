from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.user_schema import (
    UserCreate, UserUpdate, UserStatusUpdate,
    UserResponse, UserListResponse,
)
from app.services import user_service
from app.auth.jwt_handler import get_current_user
from app.auth.permissions import require_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user (admin only)",
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.create_user(db, payload)


@router.get(
    "",
    response_model=UserListResponse,
    summary="List all users with optional filters (admin only)",
)
def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    role: Optional[UserRole] = Query(None, description="Filter by role"),
    user_status: Optional[UserStatus] = Query(None, alias="status", description="Filter by status"),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.list_users(db, page=page, limit=limit, role=role, status=user_status)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get your own profile (all authenticated roles)",
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """Returns the profile of whoever is currently authenticated."""
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get a user by ID (admin only)",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.get_user_by_id(db, user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update a user's details (admin only)",
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.update_user(db, user_id, payload)


@router.patch(
    "/{user_id}/status",
    response_model=UserResponse,
    summary="Activate or deactivate a user (admin only)",
)
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.update_user_status(db, user_id, payload)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a user (admin only)",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user_service.delete_user(db, user_id)
