from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from src.core.dependencies import get_auth_service
from src.core.exceptions import InvalidCredentialsError, UserInactiveError
from src.core.security import create_access_token
from src.schemas.user import UserCreate, UserResponse, UserLogin
from src.services.auth import AuthService
from src.services.email import EmailService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        background_tasks: BackgroundTasks,
        auth_service: AuthService = Depends(get_auth_service),

):
    try:
        user = await auth_service.register_user(user_data)

        background_tasks.add_task(
            EmailService.enqueue_email_task,
            email=user.email
        )

        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(
        credentials: UserLogin,
        auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = await auth_service.authenticate_user(
            email=credentials.email,
            password=credentials.password
        )

        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="User inactive")

        token_data = {"sub": str(user.id)}
        token = create_access_token(token_data)

        return {"access_token": token, "token_type": "bearer"}

    except InvalidCredentialsError:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    except UserInactiveError:
        raise HTTPException(status_code=400, detail="User inactive")
