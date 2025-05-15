from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class DatabaseConfig(BaseModel):
    url: PostgresDsn = ""
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class RedisConfig(BaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    EMAIL_QUEUE_NAME: str = "email_queue"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix="APP_",
        case_sensitive=False,
        env_nested_delimiter="_"
    )

    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()


settings = AppSettings()
