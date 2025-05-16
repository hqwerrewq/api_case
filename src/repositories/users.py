from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.types.repositories import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, is_active: bool = True) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            is_active=is_active
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
