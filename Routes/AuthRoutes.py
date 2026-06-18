from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from Config.Database import get_db
from Models.UserModel import User
from Schemas.UserSchema import UserCreate, UserResponse

from Config.AuthConfig import verify_password, get_password_hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # parse created_at if provided as ISO string
    created_at_val = None
    try:
        if getattr(user, "created_at", None):
            created_at_val = datetime.fromisoformat(user.created_at)
    except Exception:
        created_at_val = None

    new_user = User(
        full_name=user.full_name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        created_at=created_at_val,
        role=getattr(user, "role", "user")
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful!"}
