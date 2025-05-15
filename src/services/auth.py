from passlib.context import CryptContext

from src.core.exceptions import InvalidCredentialsError, UserInactiveError
from src.models import User
from src.repositories.users import UserRepository
from src.schemas.user import UserCreate


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def register_user(self, user_data: UserCreate) -> User:
        if await self.user_repo.get_by_email(user_data.email):
            raise ValueError("User with this email already exists")

        hashed_password = self.pwd_context.hash(user_data.password)
        return await self.user_repo.create(
            email=user_data.email,
            password_hash=hashed_password,
            is_active=True
        )

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise InvalidCredentialsError()
        if not user.is_active:
            raise UserInactiveError()
        if not user.verify_password(password):
            raise InvalidCredentialsError()
        return user


