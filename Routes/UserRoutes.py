from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from Config.Database import get_db
from Models.UserModel import User
from fastapi import HTTPException
from Schemas.UserSchema import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# get all users
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# get user by id
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#update user by id
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.full_name = user.full_name
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

#delete user by id
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"} 