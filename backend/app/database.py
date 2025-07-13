import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
from .config import settings

logger = logging.getLogger(__name__)

# Create async engine with proper configuration
# Ensure we use asyncpg driver for async operations
database_url = settings.DATABASE_URL
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif not database_url.startswith("postgresql+asyncpg://"):
    # If it's already postgresql+something, replace with asyncpg
    if "postgresql+" in database_url:
        database_url = database_url.replace("postgresql+", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=5 if os.getenv('TESTING') == 'true' else 10,  # Smaller pool for testing
    max_overflow=10 if os.getenv('TESTING') == 'true' else 20,  # Smaller overflow for testing
    pool_recycle=1800 if os.getenv('TESTING') == 'true' else 3600,  # Shorter recycle for testing
    pool_timeout=30,  # Add explicit timeout
    connect_args={
        "server_settings": {
            "application_name": "qpesapay_test" if os.getenv('TESTING') == 'true' else "qpesapay",
        }
    } if os.getenv('TESTING') == 'true' else {},
    echo=settings.LOG_LEVEL == "DEBUG"
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """
    Dependency to get database session with proper error handling.
    """
    async with SessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await session.rollback()
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def check_db_connection():
    """
    Check database connection health.
    """
    try:
        async with SessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

async def wait_for_db_ready(max_retries: int = 30, retry_delay: float = 1.0):
    """
    Wait for database to be ready with retries.
    Useful for CI/CD environments where database might not be immediately available.
    """
    import asyncio

    for attempt in range(max_retries):
        if await check_db_connection():
            logger.info(f"Database connection established on attempt {attempt + 1}")
            return True

        if attempt < max_retries - 1:
            logger.warning(f"Database not ready, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
            await asyncio.sleep(retry_delay)

    logger.error(f"Database connection failed after {max_retries} attempts")
    return False