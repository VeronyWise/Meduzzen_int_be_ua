from pydantic import BaseModel, EmailStr
from typing import  Optional
from datetime import date, datetime, time, timedelta


class CompanyBase(BaseModel):
    id: int    
    name: str
    is_hidden: bool
    description: str
    owner_id: int
    creation_data: datetime

    class Config:
        orm_mode = True

class CompanyOwner(CompanyBase):
    pass
    class Config:
        orm_mode = True

class CompanyCreat(CompanyBase):
    owner: str 
    class Config:
        orm_mode = True

class CompanyUpdate(CompanyBase):
    pass
class Config:
        orm_mode = True

class CompanyList(CompanyBase):
    list: list

    class Config:
        orm_mode = True