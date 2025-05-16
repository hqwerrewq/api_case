from typing import Protocol

from src.models.user import User


class IUserRepository(Protocol):

    async def get_by_id(self, user_id: int) -> User | None:
        ...

    async def get_by_email(self, email: str) -> User | None:
        ...

    async def create(self, email: str, password_hash: str, is_active: bool) -> User:
        ...
