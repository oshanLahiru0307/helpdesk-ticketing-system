from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from Config.auth_config import get_password_hash, verify_password
from Config.settings import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from core.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from Models.user import User
from repositories.repository import repository
from Schemas.user_schema import UserCreate, UserLogin, UserUpdate


class JwtService:
    """JWT token creation and validation."""

    @staticmethod
    def create_access_token(user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {"sub": str(user_id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def get_user_id_from_token(token: str) -> int:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise JWTError("Token missing user id")
        return int(user_id)


class UserService:
    """Business logic for user CRUD operations."""

    def create_user(self, db: Session, request: UserCreate) -> User:
        if repository.get_user_by_email(db, request.email):
            raise BadRequestException("Email already registered")

        if repository.get_user_by_username(db, request.username):
            raise BadRequestException("Username already taken")

        user = User(
            full_name=request.full_name,
            username=request.username,
            email=request.email,
            password=get_password_hash(request.password),
            created_at=datetime.now(),
            role=request.role,
        )
        return repository.create_user(db, user)

    def get_all_users(self, db: Session) -> list[User]:
        return repository.get_all_users(db)

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return repository.get_user_by_id(db, user_id)

    def update_user(
        self, db: Session, user_id: int, request: UserUpdate
    ) -> User | None:
        user = repository.get_user_by_id(db, user_id)
        if not user:
            return None

        update_data = {
            key: value
            for key, value in request.model_dump().items()
            if value is not None
        }

        if not update_data:
            raise NotFoundException("User not found or no changes made")

        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])

        for key, value in update_data.items():
            setattr(user, key, value)

        return repository.update_user(db, user)

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = repository.get_user_by_id(db, user_id)
        if not user:
            return False

        repository.delete_user(db, user)
        return True


class AuthService:
    """Business logic for registration and login."""

    def register(self, db: Session, request: UserCreate) -> User:
        return user_service.create_user(db, request)

    def login(self, db: Session, credentials: UserLogin) -> str:
        user = repository.get_user_by_email(db, credentials.email)
        if not user or not verify_password(credentials.password, user.password):
            raise UnauthorizedException("Invalid email or password")

        return JwtService.create_access_token(user.id)


user_service = UserService()
auth_service = AuthService()
