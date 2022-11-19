from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from ..crud import auth 
from app.schemas.user import Token, UserCreate
from app.db.db import get_db
from app.crud import AuthService, get_current_user
from app.routers.user import UserBase
import os 
from fastapi_auth0 import Auth0
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User


auth_router = APIRouter()
token_auth_schema = HTTPBearer()
auth0_domain = os.getenv('AUTH0_DOMAIN', '')
auth0_api_audience = os.getenv('AUTH0_API_AUDIENCE', '')
auth = Auth0(domain=auth0_domain, api_audience=auth0_api_audience)


@auth_router.post('/login', response_model=Token)
async def login( auth_data: OAuth2PasswordRequestForm = Depends(),
                 db: AsyncSession = Depends(get_db)) -> UserBase:
    return await AuthService(db).authenticate_user(auth_data.username, auth_data.password)

@auth_router.get("/me", response_model=UserBase)
async def get_me(user: User = Depends(get_current_user)) -> UserBase:
    return UserBase(**jsonable_encoder(user))

@auth_router.post("/sign-up/", response_model=Token, status_code=status.HTTP_201_CREATED)
async def sign_up(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    return await AuthService(db).register_new_user(user_data)


    