import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')

database = databases.Database(DATABASE_URL)

engine = create_async_engine(DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'))
metadata = MetaData()

Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# session call to db for every request to specific 
# def get_db():
#     db = Session()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()