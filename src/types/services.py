from typing import Protocol

from src.models.user import User
from src.schemas.user import UserCreate


class IAuthService(Protocol):

    async def register_user(self, user_data: UserCreate) -> User:
        ...

    async def authenticate_user(self, email: str, password: str) -> User:
        ...


class IEmailService(Protocol):

    async def send_welcome_email(self, email: str) -> None:
        ...

    async def enqueue_email_task(self, email: str) -> None:
        ...
