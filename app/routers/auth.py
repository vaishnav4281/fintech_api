<<<<<<< HEAD
from fastapi import APIRouter, Depends
=======
from fastapi import APIRouter, Depends, status
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
<<<<<<< HEAD
from app.services.user_service import authenticate_user
=======
from app.services import user_service
from app.schemas.user_schema import UserCreate, UserResponse, LoginRequest
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


@router.post(
<<<<<<< HEAD
=======
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account (public)",
)
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Public registration endpoint. 
    In a real app, you would restrict who can register as an 'admin'.
    """
    return user_service.create_user(db, payload)


@router.post(
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and obtain a JWT access token",
)
def login(
<<<<<<< HEAD
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Submit `username` (email) and `password` via form data.
    Returns a Bearer token valid for the configured expiry window.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
=======
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Submit `email` and `password` via JSON body.
    Returns a Bearer token valid for the configured expiry window.
    """
    user = user_service.authenticate_user(db, payload.email, payload.password)
>>>>>>> fb8f58e (Initialize project with full API features and documentation)
    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer", "role": user.role.value}
