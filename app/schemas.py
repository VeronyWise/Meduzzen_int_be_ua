from pydantic import BaseModel, EmailStr
from typing import  Optional


# model responsible for validating the request body:
class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str


class UserCreate(UserBase):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    hashed_password: str
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: Optional[str] = None
    is_active: bool = True
    class Config:
        orm_mode = True

