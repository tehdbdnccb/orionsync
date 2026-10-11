from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config.settings import get_settings
from src.utils.logger import log

settings = get_settings()

# Ensure the database URL uses the asyncpg driver (e.g., postgresql+asyncpg://)
# If using a standard Supabase URL, replace 'postgresql://' with 'postgresql+asyncpg://'
db_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Create a robust async engine optimized for high-concurrency
engine = create_async_engine(
    db_url,
    echo=settings.debug,          # Logs raw SQL queries in dev mode
    pool_size=10,                 # Base number of connections
    max_overflow=20,              # Allow bursting for traffic spikes
    pool_timeout=30,              # Guard application threads
    pool_pre_ping=True            # Detect dead connections before executing
)

# Explicitly use async_sessionmaker and disable expire_on_commit
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 declarative models"""
    pass

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for injecting database sessions per request.
    Ensures sessions are closed safely even if an endpoint crashes.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            log.error(f"Database transaction failed and rolled back: {e}")
            raise
        finally:
            await session.close()