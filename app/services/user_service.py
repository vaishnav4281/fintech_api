from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.models.user import User, UserRole, UserStatus
from app.schemas.user_schema import UserCreate, UserUpdate, UserStatusUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ── CRUD ─────────────────────────────────────────────────────────────────────

def create_user(db: Session, payload: UserCreate) -> User:
    if db.query(User).filter(User.email == payload.email, User.is_deleted == False).first():  # noqa: E712
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{payload.email}' is already registered.",
        )
    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        status=UserStatus.active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()  # noqa: E712
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email, User.is_deleted == False).first()  # noqa: E712


def list_users(
    db: Session,
    page: int = 1,
    limit: int = 20,
    role: Optional[UserRole] = None,
    status: Optional[UserStatus] = None,
) -> dict:
    query = db.query(User).filter(User.is_deleted == False)  # noqa: E712
    if role:
        query = query.filter(User.role == role)
    if status:
        query = query.filter(User.status == status)

    total = query.count()
    items = query.order_by(User.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    return {"total": total, "page": page, "limit": limit, "items": items}


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)

    # Check email uniqueness if changing
    if payload.email and payload.email != user.email:
        if db.query(User).filter(User.email == payload.email, User.is_deleted == False).first():  # noqa: E712
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{payload.email}' is already in use.",
            )
        user.email = payload.email

    if payload.name is not None:
        user.name = payload.name
    if payload.role is not None:
        user.role = payload.role
    if payload.password is not None:
        user.password_hash = hash_password(payload.password)

    db.commit()
    db.refresh(user)
    return user


def update_user_status(db: Session, user_id: int, payload: UserStatusUpdate) -> User:
    user = get_user_by_id(db, user_id)
    user.status = payload.status
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    """Soft-delete: marks is_deleted=True instead of removing the row."""
    user = get_user_by_id(db, user_id)
    user.is_deleted = True
    db.commit()


# ── Auth helper ──────────────────────────────────────────────────────────────

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.status.value == "inactive":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Contact an administrator.",
        )
    return user
