# import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')
# db_user = os.getenv('DB_USER')
# db_passwoord = os.getenv('DB_PASSWORD')
# db_name = os.getenv('DB_NAME')
# db_host = os.getenv('DB_HOST')

# DATABASE_URL = 'postgresql://{db_user}:{db_passwoord}@{db_host}:5432/{db_name}'
# database = databases.Database(DATABASE_URL)
# engine = create_engine(DATABASE_URL)

# ASYNC_DATABASE_URL = 'postgresql+asyncpg://{db_user}:{db_passwoord}@{db_host}:5432/{db_name}'
# engine = create_async_engine(ASYNC_DATABASE_URL)
engine = create_async_engine(DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'))
metadata = MetaData()

Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()
