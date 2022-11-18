from fastapi import Depends, APIRouter, Body, HTTPException
from starlette import status
from app.db.db import get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Company, User
from fastapi.security import HTTPBearer
from app.crud.statements import StatementsService

from app.schemas.statements import StatementsBase, StatementsCompany, StatementsUser, CreatStatements
from app.crud import get_current_user, get_owner, get_owner_or_admin
from app.models.user import User, Company, UserType, JoinStatement


token_auth_schema = HTTPBearer()
statements_router = APIRouter()

@statements_router.get("/company/{company_id}/statements/", response_model=Page[StatementsCompany], status_code=status.HTTP_200_OK)
async def get_company_statements(company_id:int, session: AsyncSession = Depends(get_db), 
                              params: Params = Depends(),
                              company: User = Depends(get_current_user)):
     statements = await StatementsService(session=session).get_company_statements(company_id=company_id)
     return paginate(params=params, sequence=[StatementsCompany(**company.__dict__) for company in statements],)
     
@statements_router.get("/user/{user_id}/statements/", response_model=Page[StatementsUser], status_code=status.HTTP_200_OK)
async def get_user_statements(user_id:int, session: AsyncSession = Depends(get_db),
                              params: Params = Depends(),
                              company: User = Depends(get_current_user)):
     statements = await StatementsService(session=session).get_users_statements(user_id=user_id)
     return paginate(params=params, sequence=[StatementsUser(**user.__dict__) for user in statements],)


@statements_router.post("/company/{company_id}/statements/", response_model=CreatStatements, status_code=status.HTTP_201_CREATED)
async def statement_to_company(company_id:int, current_user: User= Depends(get_owner), 
                              session: AsyncSession = Depends(get_db)) -> CreatStatements:
     result = await StatementsService(session=session).creat_statements_to_company(company_id=company_id, 
               current_user=current_user)
     return CreatStatements(**result.__dict__)


@statements_router.patch("/statements/{id}", response_model=StatementsBase, status_code=status.HTTP_201_CREATED)
async def update_statements(id:int, statements:StatementsBase, session: AsyncSession = Depends(get_db),
                         current_user: User= Depends(get_owner)) ->StatementsBase:
     result = await StatementsService(session=session).update_statements(statements_data=statements, id=id, current_user=current_user)
     return StatementsBase(**result.__dict__)

@statements_router.delete('/statement/{id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id:int, session: AsyncSession = Depends(get_db),
                         current_user: User= Depends(get_owner)):
     result = await StatementsService(session=session).delete_statements(id=id)

