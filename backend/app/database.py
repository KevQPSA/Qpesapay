from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
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
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
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