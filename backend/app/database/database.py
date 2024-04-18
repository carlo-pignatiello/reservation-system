from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

user = os.getenv("POSTGRES_USER", "NA")
password = os.getenv("POSTGRES_PASSWORD", "NA")
database = os.getenv("POSTGRES_DATABASE", "NA")
host = os.getenv("POSTGRES_HOST", "NA")
port = os.getenv("POSTGRES_PORT", "NA")

db_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

engine = create_async_engine(
    db_url, pool_size=20, pool_pre_ping=True, pool_recycle=3600
)


async def init_db():
    """Async method that initialize db instance"""
    async with engine.begin() as conn:
        # this doesnt execute asynchronously,
        # so we used run_sync to execute it synchronously within the async function.
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator:
    """Get Async session

    Returns:
        AsyncSession: Async session for MySQL

    Yields:
        Iterator[AsyncSession]: Async session for MySQL
    """
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
