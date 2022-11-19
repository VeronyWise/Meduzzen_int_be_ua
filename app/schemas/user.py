from pydantic import BaseModel, EmailStr
from typing import  Optional
from typing import List, Union
from app.schemas.company import CompanyOwner
from enum import Enum


class UserType(str, Enum):
    admin = "1"
    regular = "2"
    owner = "3"

# model responsible for validating the request body:
class UserBase(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: str
    id: int


class UserCreate(UserBase):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr
    hashed_password: Optional[str] = None
    user_type: UserType 
    class Config:
        orm_mode = True

class UserIn(BaseModel):
    firstname: str 
    lastname: str
    username: str
    password: Optional[str] = None
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstname: str = None
    lastname: str = None
    username: str = None
    password: Optional[str] = None
    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode: True

class UserLogout(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode: True

class UserId(UserBase):
    id: int
    class Config:
        orm_mode: True

class UserList(UserBase):
    id: int
    is_active: bool


    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    username: str
    email: str
    is_active: bool
    user_type: UserType 


    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

class TokenData(BaseModel):
    id: Optional[str] = None