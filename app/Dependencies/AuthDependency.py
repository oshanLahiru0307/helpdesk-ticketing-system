from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from Config.Database import get_db
from Models.UserModel import User
from Services.JwtService import JwtService
from Services.UserService import UserService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate the JWT token and return the matching user from the database.
    Raises 401 if the token is invalid or the user no longer exists.
    """
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = JwtService.get_user_id_from_token(credentials.credentials)
    except JWTError:
        raise invalid_credentials

    user_service = UserService(db)
    try:
        return user_service.get_by_id(user_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            raise invalid_credentials
        raise
