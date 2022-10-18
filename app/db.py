import databases
from sqlalchemy import create_engine, MetaData


DATABASE_URL = "postgresql://postgres:password@postgres_med:5432/meduzz_db"

database = databases.Database(DATABASE_URL)


#  creating the tables in the same Python file, but in production, 
# you would probably want to create them with Alembic, integrated with migrations
# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False})

# metadata = MetaData()
# metadata.create_all(engine)