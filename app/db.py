import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv
import os

#знайти дотенв файл і підтягувати налаштування
load_dotenv(find_dotenv())

DATABASE_URL = os.getenv('DATABASE_URL')

database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

metadata = MetaData()

# ORM session factory bound to this engine,and a base class for our classes definitions.
Session = sessionmaker(bind=engine)
Base = declarative_base()