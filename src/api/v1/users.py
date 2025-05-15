from fastapi import APIRouter, Depends

from src.core.security import get_current_user
from src.models import User
from src.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(
        current_user: User = Depends(get_current_user)
):
    return current_user
