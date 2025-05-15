from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users import UserRepository
from src.services.auth import AuthService
from .db import db_dependency


async def get_user_repository(
    db: AsyncSession = Depends(db_dependency.get_db)
) -> UserRepository:
    return UserRepository(db)

async def get_auth_service(
    repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
    return AuthService(repo)