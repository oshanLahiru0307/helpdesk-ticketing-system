from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.dependencies import get_db
from Schemas.user_schema import Token, UserCreate, UserLogin, UserResponse
from Services.service import auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
def register(request: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register(db, request)


@router.post("/login", response_model=Token)
def login(request: UserLogin, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, request)
    return Token(access_token=access_token)
