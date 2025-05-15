from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .config import settings


class DatabaseDependency:
    def __init__(self, database_url: str, echo: bool = False, pool_size: int = 5, max_overflow: int = 10):

        self.engine = create_async_engine(
            database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session


db_dependency = DatabaseDependency(
    database_url=str(settings.database.url),
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
)
