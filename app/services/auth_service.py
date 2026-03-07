from fastapi import HTTPException

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserCreate
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, payload: UserCreate) -> User:
        if self.user_repository.get_by_email(payload.email):
            raise ValueError("User with this email already exists")

        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password[:72]),
            full_name=payload.full_name,
        )  # Hashing should be done here
        return self.user_repository.create(user)

    def login(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"sub": str(user.id)})
        return token
