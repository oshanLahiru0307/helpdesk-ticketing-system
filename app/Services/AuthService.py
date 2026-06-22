from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from Models.UserModel import User
from Schemas.UserSchema import UserCreate, UserLogin
from Services.JwtService import JwtService
from Services.UserService import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Business logic for registration and login."""

    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)

    def register(self, user_data: UserCreate) -> User:
        """Create a new user account (delegates to UserService.create)."""
        return self.user_service.create(user_data)

    def login(self, credentials: UserLogin) -> str:
        """Verify credentials and return a JWT access token."""
        user = self.db.query(User).filter(User.email == credentials.email).first()
        if not user or not pwd_context.verify(credentials.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        return JwtService.create_access_token(user.id)
