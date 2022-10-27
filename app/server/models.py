from enum import unique
from sqlalchemy import String, Integer, Column, Boolean
import sqlalchemy
from app.db import Base
from sqlalchemy.ext.declarative import declarative_base
from app.db import metadata


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    username = Column(String(150))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True,
     server_default=sqlalchemy.sql.expression.true(), nullable=True,)
 
users = User.__table__
