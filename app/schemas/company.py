from pydantic import BaseModel, EmailStr
from typing import  Optional
from datetime import date, datetime, time, timedelta
# from app.schemas.user import User


class CompanyBase(BaseModel):  
    name: str
    is_hidden: bool
    description: Optional[str] = None
    owner_id: int

    # creation_data: datetime

    class Config:
        orm_mode = True


class CompanyOwner(CompanyBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class CompanyCreate(CompanyBase):
    class Config:
        orm_mode = True

class CompanyUpdate(CompanyBase):
    pass
class Config:
        orm_mode = True

class CompanyList(CompanyBase):
    id: int
    class Config:
        orm_mode = True

class JSSchemas(BaseModel):
    id: int
    user_id: int
    company_id: int
    is_accepted: bool
    # typy_employee: str

    class Config:
        orm_mode = True