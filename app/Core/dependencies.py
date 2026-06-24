from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from Config.database import SessionLocal
from Models.user import User
from Repositories.repository import repository
from Services.service import JwtService

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Validate JWT token and return the authenticated user."""
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = JwtService.get_user_id_from_token(credentials.credentials)
    except JWTError:
        raise invalid_credentials

    user = repository.get_user_by_id(db, user_id)
    if not user:
        raise invalid_credentials

    return user
