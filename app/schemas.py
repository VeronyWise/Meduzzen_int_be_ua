from pydantic import BaseModel, EmailStr
from typing import List

# model responsible for validating the request body:
class UserBase(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str

class UserCreate(UserBase):
    pass
    email: EmailStr
    username: str
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: EmailStr
    username: str
    class Config:
        orm_mode = True

class UserInDB(UserBase):
    id: int
    class Config:
        orm_mode = True

class UserList(UserBase):
    id: int
    is_active: bool
    users: List[UserBase] = []
