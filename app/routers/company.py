from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from app.db.db import engine, metadata, get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Company, User
from fastapi.security import HTTPBearer
from app.crud.auth import AuthService
from app.crud.company import CompanyService
from app.crud.user import UserService
from app.crud.member import MemberService

from app.schemas.company import CompanyBase, CompanyCreate, CompanyList, CompanyUpdate
from app.crud import get_current_user, get_owner, get_owner_or_admin



token_auth_schema = HTTPBearer()
company_router = APIRouter()


@company_router.get('/companies/', response_model=Page[CompanyList], status_code=status.HTTP_200_OK)
async def get_company(session: AsyncSession = Depends(get_db), params: Params = Depends(),
                        company: User = Depends(get_current_user)) -> Page[CompanyList]:
    all_company = await CompanyService(session=session).get_companies()
    return paginate(params=params, sequence= [CompanyList(**company.__dict__) for company in all_company],)

@company_router.post("/company/", response_model=CompanyCreate, status_code=status.HTTP_201_CREATED)
async def creat_company(company: CompanyCreate, session: AsyncSession = Depends(get_db), 
                         current_user: User= Depends(get_owner)) -> CompanyCreate:
    companies = await CompanyService(session=session).creat_company(company_data=company, current_user=current_user)
    return CompanyCreate(**companies.__dict__)

@company_router.patch("/company/{id}", response_model=CompanyBase, status_code=status.HTTP_201_CREATED)
async def update_company(id:int, company:CompanyBase, session: AsyncSession = Depends(get_db), 
                         current_user: User= Depends(get_owner)) -> CompanyCreate:
    result = await CompanyService(session=session).update_company(company=company, id=id, current_user=current_user)
    return CompanyCreate(**result.__dict__)
    
@company_router.delete("/company/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company_by_owner(company_id:int, session: AsyncSession= Depends(get_db),
                         company: Company = Depends(get_owner)):
    return await  CompanyService(session=session).delete_company(id=company_id)

@company_router.delete("/companies/{company_id}/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_from_company(company_id:int, user_id:int, session: AsyncSession= Depends(get_db),
                         owner: User = Depends(get_owner)):
    company = await CompanyService(session=session).get_company_by_id(id=company_id)
    if company.owner_id != owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user = await UserService(session=session).get_user(user_id=user_id)
    return await  MemberService(session=session).delete_user(company=company, user=user)


