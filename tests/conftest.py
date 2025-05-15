from unittest.mock import AsyncMock

import pytest
from passlib.context import CryptContext

from src.models.user import User
from src.repositories.users import UserRepository
from src.services.auth import AuthService


@pytest.fixture
def mock_user_repo():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(mock_user_repo)


@pytest.fixture
def sample_user():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return User(
        id=1,
        email="test@example.com",
        password_hash=pwd_context.hash("password123"),
        is_active=True
    )
