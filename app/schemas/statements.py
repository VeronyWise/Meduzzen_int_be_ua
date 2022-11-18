from pydantic import BaseModel, EmailStr
from typing import  Optional
from datetime import date, datetime, time, timedelta

class StatementsBase(BaseModel):
     is_accepted: bool

class CreatStatements(BaseModel):
     company_id: int

     class Config:
          orm_mode = True

class StatementsUser(StatementsBase):
     id: int
     user_id: int

     class Config:
          orm_mode = True


class StatementsCompany(StatementsBase):
     id: int
     company_id: int
     user_id: int
     is_accepted: bool

     class Config:
          orm_mode = True
