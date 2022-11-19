from fastapi import Depends, APIRouter, Body, HTTPException
from starlette import status
from app.db.db import get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Company, User
from fastapi.security import HTTPBearer
from app.crud.statements import StatementsService

from app.schemas.statements import StatementsBase, StatementsCompany, CreatStatementsUser, CreatStatements
from app.crud import get_current_user, get_owner, get_owner_or_admin
from app.models.user import User, Company, UserType, JoinStatement


token_auth_schema = HTTPBearer()
statements_router = APIRouter()

@statements_router.get("/companies/{company_id}/statements/", response_model=Page[StatementsCompany], status_code=status.HTTP_200_OK)
async def get_company_statements(company_id:int, session: AsyncSession = Depends(get_db), 
                              params: Params = Depends(),
                              user: User = Depends(get_owner_or_admin)):
     statements = await StatementsService(session=session).get_company_statements(company_id=company_id)
     return paginate(params=params, sequence=[StatementsCompany(**company.__dict__) for company in statements],)
     
@statements_router.get("/users/statements/", response_model=Page[StatementsCompany], status_code=status.HTTP_200_OK)
async def get_user_statements(user_id:int, session: AsyncSession = Depends(get_db),
                              params: Params = Depends(),
                              company: User = Depends(get_current_user)):
     statements = await StatementsService(session=session).get_users_statements(user_id=user_id)
     return paginate(params=params, sequence=[StatementsCompany(**user.__dict__) for user in statements],)
# from user to company
@statements_router.post("/users/statements/", response_model=CreatStatementsUser, status_code=status.HTTP_200_OK)
async def statement_to_company(body: CreatStatementsUser, 
                              current_user: User= Depends(get_current_user), 
                              session: AsyncSession = Depends(get_db)):
     result = await StatementsService(session=session).creat_statements_to_company(current_user=current_user,
                                                  company_id=body.company_id)
     return CreatStatementsUser(**result.__dict__)

#from company to user
@statements_router.post("/companies/{company_id}/statements/", response_model=CreatStatements, status_code=status.HTTP_201_CREATED)
async def statement_to_company(company_id:int, body: CreatStatements,
                              current_user: User= Depends(get_owner_or_admin), 
                              session: AsyncSession = Depends(get_db)) -> CreatStatements:
     result = await StatementsService(session=session).creat_statements_from_company(company_id=company_id, 
                                                            user_id=body.user_id)
     return CreatStatements(**result.__dict__)


@statements_router.patch("/statements/{pk}", response_model=StatementsBase, status_code=status.HTTP_201_CREATED)
async def update_statements(pk:int, statements:StatementsBase, session: AsyncSession = Depends(get_db),
                         current_user: User= Depends(get_owner_or_admin)) ->StatementsBase:
     result = await StatementsService(session=session).update_statements(statement_status=statements.status, statement_id=pk)
     return StatementsBase(**result.__dict__)



