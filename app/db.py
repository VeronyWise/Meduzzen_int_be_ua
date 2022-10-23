import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://postgres:password@postgres_med:5432/meduzz_db"

database = databases.Database(DATABASE_URL)

# Alembic, integrated with migrations SQLAlchemy Engine that will interact with our dockerized PostgreSQL database
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})

Session = sessionmaker(bind=engine)
Base = declarative_base()

metadata = MetaData()
metadata.create_all(engine)

# ORM session factory bound to this engine,
# and a base class for our classes definitions.

# session call to db for every request to specific 
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()