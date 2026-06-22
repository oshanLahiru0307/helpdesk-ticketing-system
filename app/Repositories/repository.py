from sqlalchemy.orm import Session

from Models.user import User


class UserRepository:
    """Database access layer — only talks to the database, no business rules."""

    def create_user(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all_users(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_user_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    def update_user(self, db: Session, user: User) -> User:
        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()


repository = UserRepository()
