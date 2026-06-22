from datetime import datetime

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from Models.UserModel import User
from Schemas.UserSchema import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Business logic for user CRUD — mirrors your Customer collection operations."""

    def __init__(self, db: Session):
        self.db = db

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def create(self, user_data: UserCreate) -> User:
        """Create a new user (like insert_one in your Customer example)."""
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        if self.db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")

        new_user = User(
            full_name=user_data.full_name,
            username=user_data.username,
            email=user_data.email,
            password=self._hash_password(user_data.password),
            created_at=datetime.now(),
            role=user_data.role,
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_all(self) -> list[User]:
        """Return all users (like find().to_list() in your Customer example)."""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        """Find one user by ID (like find_one with _id)."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update(self, user_id: int, user_data: UserUpdate) -> User:
        """
        Update only the fields that were sent (same pattern as UpdateCustomer).
        Raises 404 if the user does not exist or no changes were made.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = {
            key: value
            for key, value in user_data.model_dump().items()
            if value is not None
        }

        if not update_data:
            raise HTTPException(
                status_code=404, detail="User not found or no changes made"
            )

        if "password" in update_data:
            update_data["password"] = self._hash_password(update_data["password"])

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """
        Delete a user by ID (like delete_one in your Customer example).
        Returns True if deleted, False if not found.
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
