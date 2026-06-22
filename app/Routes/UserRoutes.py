from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from Config.Database import get_db
from Dependencies.AuthDependency import get_current_user
from Models.UserModel import User
from Models.UserSerializer import user_serializer
from Schemas.UserSchema import UserCreate, UserUpdate
from Services.UserService import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Create User
@router.post("/create_new_user")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    new_user = user_service.create(user)
    return user_serializer(new_user)


# Get All Users
@router.get("/get_all_users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    users = user_service.get_all()
    return [user_serializer(u) for u in users]


# Get current logged-in user
@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return user_serializer(current_user)


# Get Single User
@router.get("/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    user = user_service.get_by_id(user_id)
    return user_serializer(user)


# Update User
@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    updated_user = user_service.update(user_id, user)
    return user_serializer(updated_user)


# Delete User
@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_service = UserService(db)
    deleted = user_service.delete(user_id)

    if deleted:
        return {"message": "User deleted successfully"}

    raise HTTPException(status_code=404, detail="User not found")
