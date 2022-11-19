from fastapi import HTTPException, Depends
from starlette import status
from app.models.user import User, Company, UserType, JoinStatement, StatementType
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from app.crud.base_session import BaseSession
from app.crud import get_current_user
from app.crud.user import UserService
from app.crud.company import CompanyService
from app.schemas.statements import AcceptedInCompany
from app.models.enummodels import StatementType, UserType
from app.models.user import keywords_tables


class MemberService(BaseSession):

     """Member by id"""

     async def add_member(self, statement: JoinStatement):
          company = await CompanyService(session=self.session).get_company_by_id(id=statement.company_id)
          user = await UserService(session=self.session).get_user(user_id=statement.user_id)
          user.companies.append(company)
          await self.session.commit()


     async def delete_user(self, company:Company, user:User):
          try:
               user.companies.remove(company)
          except ValueError:
               pass
          await self.session.commit()
