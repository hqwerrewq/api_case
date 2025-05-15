from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)


    def verify_password(self, password: str) -> bool:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }
