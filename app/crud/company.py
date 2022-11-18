from fastapi import HTTPException, Depends
from requests import session
from starlette import status
from app.models.user import User, Company, UserType, JoinStatement
from app.schemas.company import CompanyBase, CompanyCreate, CompanyList, CompanyOwner, CompanyUpdate, JSSchemas
from hashlib import sha256
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
import re
from app.crud.base_session import BaseSession
from app.crud import get_current_user
from app.crud.user import UserService
from app.models.enummodels import StatementType, UserType


class CompanyService(BaseSession):

     async def get_current_admin(user: User = Depends(get_current_user)):
          if user.user_type != UserType('1'):
               raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access!")
          return user

     async def get_companies(self) -> List[Company]:
          company_all = await self.session.execute(select(Company).where(Company.is_hidden==False))
          return company_all.scalars().all()

     async def get_company_by_id(self, id:int):
          company = await self.session.execute(select(Company).where(Company.id==id))
          company: Company = company.scalars().one_or_none()
          return company 

     async def get_company_by_name(self, name:str):
          company = await self.session.execute(select(Company).where(Company.name == name))
          company: Company = company.scalars().one_or_none()
          return company

     async def get_company_by_ownerid(self, owner_id:int)->List[Company]:
          company = await self.session.execute(select(Company).where(Company.owner_id==owner_id))
          company: Company = company.scalars().all()
          return company

     async def creat_company(self, company_data: CompanyCreate, current_user: User)-> Company:
          company = await self.get_company_by_name(name=company_data.name)
          if company:
               raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Company already exists")
          company_data = company_data.dict()
          company_data['owner_id'] = current_user.id
          db_company = Company(**company_data)
          self.session.add(db_company)
          await self.session.commit()
          await self.session.refresh(db_company)
          return db_company


     async def update_company(self, id:int, company: CompanyCreate, current_user: User)-> Company:
          company_in = await self.get_company_by_id(id=id)
          update_data = company.dict()
          for field in update_data:
               if field in update_data:
                    setattr(company_in, field, update_data[field])
          self.session.add(company_in)
          await self.session.commit()
          await self.session.refresh(company_in)
          return company_in




     async def get_statement(self, company_id: int, user_id: int) -> JSSchemas:
          request = await self.session.execute(select(JoinStatement).filter(JoinStatement.user_id==user_id,
                                                       JoinStatement.company_id == company_id)).scalars().one_or_none()
          if request is None:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"No request from user with id {user_id} to company with id {company_id}")
          return request

     # async def set_admin(self, owner_id: int, user_id:int,company_id:int):
     #      user = UserService(session=session).get_user(user_id=user_id)
     #      company = self.get_current_admin(company_id=company_id)


     async def delete_company(self, id: int):
          company: User = await self.get_company_by_id(id=id)
          print(company)
          if not company:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Company doesnt found!')
          await self.session.delete(company)
