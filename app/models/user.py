from enum import unique
from sqlalchemy import String, Integer, Column, Boolean, Table, Enum
import sqlalchemy
from app.db.db import Base
from sqlalchemy.ext.declarative import declarative_base
from app.db.db import metadata
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
# from sqlalchemy_utils.types.choice import ChoiceType
from enum import Enum
from sqlalchemy.dialects import postgresql
from app.models.enummodels import StatementType, UserType, StatementStatus


keywords_tables = Table(
    "company_keywords",
    Base.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("company_id", ForeignKey("companies.id"), primary_key=True),
)



class User(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    username = Column(String(150))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    creation_data = Column(DateTime)
    is_active = Column(
        Boolean, default=True,server_default=sqlalchemy.sql.expression.true(), nullable=True,
        )
    user_type = Column(postgresql.ENUM(UserType), default=UserType.owner ,nullable=False)

    companies = relationship("Company", secondary=keywords_tables, back_populates="users")
    join_statements = relationship("JoinStatement", back_populates="owner_statement") #  JS to User


class Company(Base):

    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    is_hidden = Column(Boolean, default=True, nullable=False)
    description = Column(String(255))
    owner_id = Column(Integer, ForeignKey('users.id'))
    creation_data = Column(DateTime)

    users = relationship("User", secondary=keywords_tables, back_populates="companies")
    statement_company = relationship("JoinStatement", back_populates="statement_company") # 3 JS to Company
    quizes = relationship("Quiz", back_populates="quiz_company") # 7 quiz to Company

class JoinStatement(Base):

    __tablename__ = "join_statements"
    id = Column(Integer, primary_key=True)
    user_id =  Column(Integer, ForeignKey('users.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))    
    status = Column(postgresql.ENUM(StatementStatus), default=StatementStatus.expect, nullable=True)
    type_sender = Column(postgresql.ENUM(StatementType), default=StatementType.FromUser, nullable=True) #хто відпрвив заявки

    statement_company = relationship("Company", back_populates="statement_company") # 13 JS to Company
    owner_statement = relationship("User", back_populates="join_statements") # 14 JS to User

class Quiz(Base):

    __tablename__ = "quizes"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))      
    name = Column(String(255))
    description = Column(String(255))
    periodicity = Column(Integer)
    sum_questions_by_quize = Column(Integer, nullable=False)
    sum_all_questions = Column(Integer, nullable=False)
    sum_all_correct_answers = Column(Integer, nullable=False)
    list_questions = Column(Integer)

    quiz_company = relationship("Company", back_populates="quizes")  # 8 quiz to Company
    questions = relationship("Question", back_populates="question")# 9 question to quiz

class Question(Base):

    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    quiz_id = Column(Integer, ForeignKey('quizes.id')) 

    question = relationship("Quiz", back_populates="questions") # 11 question to quiz
    answers = relationship("Answer", back_populates="answer") # 10 answer to question 

class Answer(Base):

    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    is_correct = Column(Boolean)
    qustion_id = Column(Integer, ForeignKey('questions.id')) 

    answer = relationship("Question", back_populates="answers") # 12 answer to question        
