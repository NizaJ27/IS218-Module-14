from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_password, verify_password


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password),
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        # Raise a ValueError so tests/handlers can convert to HTTP 400
        raise ValueError("username or email already exists") from e
    return user


def authenticate_user(db: Session, username: str, password: str) -> models.User:
    """Authenticate a user by username and password. Returns user if valid, None otherwise."""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def get_user_by_username(db: Session, username: str) -> models.User:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()
