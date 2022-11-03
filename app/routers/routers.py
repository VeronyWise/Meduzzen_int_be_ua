from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from app.db import engine, metadata, get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from app.server.models import User
from fastapi.security import HTTPBearer
from app.crud.auth import AuthService


from app.crud import UserService
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserIn
from app.crud import get_current_user


token_auth_schema = HTTPBearer()
# metadata.create_all(bind=engine)
user_router = APIRouter()
user_router = APIRouter(dependencies=[user_id:=Depends(token_auth_schema)])

@user_router.get("/users", response_model=Page[UserBase], status_code=status.HTTP_200_OK)
async def get_users(session: AsyncSession = Depends(get_db), params: Params = Depends(),
                    user: User = Depends(get_current_user)) -> Page[UserBase]:
     all_user = await UserService(session=session).get_all_users()
     return paginate(params=params, sequence= [UserBase(**user.__dict__) for user in all_user],)

@user_router.get("/users/{user_id}", response_model=UserBase, status_code=status.HTTP_200_OK)
async def get_one_user(user_id:int, session: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_user)):
     user = await UserService(session=session).get_user_active(user_id=user_id)
     return UserBase(**user.__dict__)

@user_router.post("/creatusers/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def creat_user(user: UserCreate, session: AsyncSession = Depends(get_db)) -> UserCreate:
     user = await UserService(session=session).create_user(serialized_data=user)
     return UserCreate(**user.__dict__)


@user_router.patch('/users/{user_id}/', response_model=UserBase, status_code=status.HTTP_200_OK)
async def update_user(
     user_id: int, 
     body: UserUpdate,
     session: AsyncSession = Depends(get_db),
     user: User = Depends(get_current_user)):
     if user_id == user.id:
          user_in = UserIn(**jsonable_encoder(user))
          if body.password is not None:
               user_in.password = body.password
          if body.firstname is not None:
               user_in.firstname = body.firstname
          if body.lastname is not None:
               user_in.lastname = body.lastname
          user = await UserService(session=session).update_user(db_user=user, serialized_user=user_in)
          return UserBase(**jsonable_encoder(user))
     raise  HTTPException(status_code=404, detail=f"User not found")

@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: int, session: AsyncSession= Depends(get_db),
                     user: User = Depends(get_current_user)):
     if user_id == user.id:
          await  UserService(session=session).delete_user(user_id=user_id)
     raise  HTTPException(status_code=404, detail=f"User not found") 

