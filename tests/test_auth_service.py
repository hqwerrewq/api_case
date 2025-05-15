import pytest

from src.core.exceptions import InvalidCredentialsError, UserInactiveError
from src.models import User
from src.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_register_user_success(auth_service, mock_user_repo):

    mock_user_repo.get_by_email.return_value = None
    mock_user_repo.create.return_value = User(id=1, email="new@example.com", is_active=True)

    user_data = UserCreate(email="new@example.com", password="strongpassword")
    result = await auth_service.register_user(user_data)

    assert result.email == "new@example.com"
    mock_user_repo.get_by_email.assert_awaited_once_with("new@example.com")
    mock_user_repo.create.assert_awaited_once()


@pytest.mark.asyncio
async def test_register_user_exists(auth_service, mock_user_repo, sample_user):

    mock_user_repo.get_by_email.return_value = sample_user

    with pytest.raises(ValueError, match="already exists"):
        await auth_service.register_user(
            UserCreate(email="test@example.com", password="password123")
        )


@pytest.mark.asyncio
async def test_authenticate_user_success(auth_service, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user

    user = await auth_service.authenticate_user(
        email="test@example.com",
        password="password123"
    )

    assert user.id == 1
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_authenticate_user_not_found(auth_service, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None

    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate_user(
            email="nonexistent@example.com",
            password="password123"
        )


@pytest.mark.asyncio
async def test_authenticate_user_inactive(auth_service, mock_user_repo, sample_user):
    sample_user.is_active = False
    mock_user_repo.get_by_email.return_value = sample_user

    with pytest.raises(UserInactiveError):
        await auth_service.authenticate_user(
            email="test@example.com",
            password="password123"
        )


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(auth_service, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user

    with pytest.raises(InvalidCredentialsError):
        await auth_service.authenticate_user(
            email="test@example.com",
            password="wrongpassword"
        )