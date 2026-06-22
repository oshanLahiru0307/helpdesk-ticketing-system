from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from Config.Database import get_db
from Models.UserSerializer import user_serializer
from Schemas.UserSchema import Token, UserCreate, UserLogin
from Services.AuthService import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Public registration — creates a new user account."""
    auth_service = AuthService(db)
    new_user = auth_service.register(user)
    return user_serializer(new_user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Log in and receive a JWT access token.
    Send it in requests as: Authorization: Bearer <access_token>
    """
    auth_service = AuthService(db)
    access_token = auth_service.login(user)
    return Token(access_token=access_token)
