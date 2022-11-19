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
from app.schemas.statements import StatementsBase, StatementsCompany, CreatStatements
from app.models.enummodels import StatementType, UserType, StatementStatus
from app.crud.member import MemberService


class StatementsService(BaseSession):


     '''Check permission for statement'''
     async def check_send_statements(self, user_id:int, company: Company,
                    statements_data:CreatStatements, owner_id:int)->bool:
          if (user_id != statements_data.user_id and user_id != company.owner_id):
               raise
          return True

     # async def type(self, user_id: int, company_id: int, statement_type: JoinStatement):
     #      if statement_type != StatementType('')

     async def get_statement_by_id(self, id: int) -> StatementsBase:
          request = await self.session.execute(select(JoinStatement).filter_by(id=id))
          request: JoinStatement = request.scalars().one_or_none()
          if not request:
               raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Request with id:{id} was not found!"
               )
          return request

     '''Send join statements to company'''
     async def creat_statements_to_company(self, company_id:int,  current_user: User):
          company = await CompanyService(session=self.session).get_company_by_id(id=company_id)
          if not company:
               raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Statement already exists")
          return await self._creat_statement(user_id=current_user.id, company_id=company.id, type_sender=StatementType.FromUser)

     '''Send join statements from company'''
     async def creat_statements_from_company(self, user_id: int, company_id:int):
          company = await CompanyService(session=self.session).get_company_by_id(id=company_id)
          user = await UserService(session=self.session).get_user(user_id=user_id)
          return await self._creat_statement(user_id=user.id, company_id=company.id, type_sender=StatementType.FromCompany)


     async def get_users_statements(self, user_id:int) ->List[StatementsCompany]:
          statement = await self.session.execute(select(JoinStatement).where(
                                                       JoinStatement.user_id==user_id))
          statement = statement.scalars().all()
          if not statement :
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"No request from to company id {user_id}")
          return statement 

     async def get_company_statements(self, company_id: int) ->List[StatementsCompany]:
          statement = await self.session.execute(select(JoinStatement).where(
                                                  JoinStatement.company_id==company_id))
          statement = statement.scalars().all()
          if statement is None:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"No request from to company id {company_id}")
          return statement 
          
     async def update_statements(self, statement_id:int, statement_status: StatementStatus):
          statement = await self.get_statement_by_id(id=statement_id)
          # if statement.status !=  StatementStatus.expect:
          #      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cant change status")
          statement.status = statement_status
          self.session.add(statement)
          await self.session.commit()
          await self.session.refresh(statement)
          # if statement.status ==  StatementStatus.confirmed:
          await MemberService(session=self.session).add_member(statement=statement)
          return statement



     async def _creat_statement(self, user_id: int, company_id:int, type_sender:StatementType):
          db_statement = JoinStatement(company_id=company_id, user_id=user_id, type_sender=type_sender)
          self.session.add(db_statement)
          await self.session.commit()
          await self.session.refresh(db_statement)
          return db_statement
     