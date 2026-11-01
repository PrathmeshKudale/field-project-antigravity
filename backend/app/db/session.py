from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.core.config import settings

_url = settings.database_url
_is_sqlite = _url.startswith("sqlite")

# SQLite does not support pool_size / max_overflow
if _is_sqlite:
    engine = create_async_engine(
        _url,
        echo=settings.debug,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_async_engine(
        _url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create tables on startup (dev only). Skips pgvector on SQLite."""
    async with engine.begin() as conn:
        if not _is_sqlite:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        import app.db.models  # noqa: F401
        from app.db.base import Base
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
