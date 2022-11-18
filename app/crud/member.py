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
from app.schemas.statements import StatementsBase, StatementsCompany, StatementsUser, CreatStatements
from app.models.enummodels import StatementType, UserType


class MemberService(BaseSession):

     """Member by id"""

     async def get_member(self, company_id: int, user_id: int):
          company = await self.session.execute(select(Company).where(Company.id==id))
          if company.

     async def delete_member(self, company_id: int, user_id: int):
          pass