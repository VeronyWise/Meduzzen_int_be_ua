from enum import unique
from sqlalchemy import String, Integer, Column, Boolean
import sqlalchemy
from app.db import Base
from sqlalchemy.ext.declarative import declarative_base


metadata = sqlalchemy.MetaData()
# Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, server_default=sqlalchemy.sql.expression.true(), nullable=False,)


users =  sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True, server_default=sqlalchemy.sql.expression.true(),
        nullable=False,))
