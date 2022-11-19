from pydantic import BaseModel
from app.models.enummodels import StatementType, StatementStatus
     

class StatementsBase(BaseModel):
     status: str


class CreatStatements(BaseModel):
     user_id: int

     class Config:
          orm_mode = True

class CreatStatementsUser(BaseModel):
     company_id: int

     class Config:
          orm_mode = True


class StatementsCompany(StatementsBase):
     id: int
     company_id: int
     user_id: int

     class Config:
          orm_mode = True


class AcceptedInCompany(StatementsBase):
     id: int
     user_id: int

     class Config:
          orm_mode = True

class AcceptedInUser(StatementsBase):
     id: int
     company_id: int

     class Config:
          orm_mode = True