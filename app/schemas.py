from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
import re
from hashlib import sha256
from fastapi import HTTPException
from starlette import status

# model responsible for validating the request body:
class UserBase(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str

# class UserPasswordCheck(BaseModel):
#     password: str

#     @validator('password')
#     def passwords_match(cls, password, **kwargs):
#         regex = r'((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,40})\S$'
#         result = re.findall(regex, password)
#         if not result:
#             raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Password must be minimum of 6 characters, at least 1 uppercase letter,'
#            '1 lowercase letter, and 1 num with no spaces.')
#         return sha256(password.encode('utf-8')).hexdigest()


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

# class UserInDB(UserBase):
#     email: EmailStr
#     class Config:
#         orm_mode = True

# class UserList(UserBase):
#     id: int
#     is_active: bool
#     users: List[UserBase] = []
