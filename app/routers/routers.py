from fastapi import Depends, APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from app.db import engine, metadata, get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.paginator import paginate
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud import UserService
from app.schemas import UserBase, UserCreate, UserUpdate



# metadata.create_all(bind=engine)
user_router = APIRouter()


@user_router.get("/users", response_model=Page[UserBase], status_code=status.HTTP_200_OK)
async def get_users(session: AsyncSession = Depends(get_db), params: Params = Depends()) -> Page[UserBase]:
     all_user = await UserService(session=session).get_all_users()
     return paginate(params=params, sequence= [UserBase(**user.__dict__) for user in all_user],)

@user_router.get("/users/{user_id}", response_model=UserBase, status_code=status.HTTP_200_OK)
async def get_one_user(user_id:int, session: AsyncSession = Depends(get_db)):
     user = await UserService(session=session).get_user_active(user_id=user_id)
     return UserBase(**user.__dict__)

@user_router.post("/creatusers/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def creat_user(user: UserCreate, session: AsyncSession = Depends(get_db)) -> UserCreate:
     user = await UserService(session=session).create_user(serialized_data=user)
     return UserCreate(**user.__dict__)

# @user_router.patch('/{user_id}', response_model=UserBase, status_code=status.HTTP_202_ACCEPTED)
# async def users(user_id: int, users: UserUpdate, password: str = Body(None),  session: AsyncSession = Depends(get_db)) -> UserUpdate:
# #     user_up = await UserService(session=session).update_user(serialized_user = serialized_user, db_user=db_user)
# #     return UserUpdate(**user_up.__dict__)
#      user_service = UserService(session=session)
#      user = await user_service.get_user_active(user_id=user_id)
#      user_in = UserUpdate(**jsonable_encoder(user))
#      if password is not None:
#           user_in.password = password
#      if users.is_active is not None:
#           user_in.is_active = users.is_active
#      if users.firstname is not None:
#           user_in.firstname = users.firstname
#      if users.lastname is not None:
#           user_in.lastname = users.lastname
#      user = await user_service.update_user(db_user=user, serialized_user=user_in)
#      return UserBase(**jsonable_encoder(user))


@user_router.patch('/users/{user_id}/', response_model=UserBase, status_code=status.HTTP_202_ACCEPTED)
async def update_user(
     user_id: int, 
     is_active: bool = Body(None),
     firstname: str = Body(None),
     lastname: str = Body(None),
     password: str = Body(None),
     session: AsyncSession = Depends(get_db)):
     user_service = UserService(session=session)
     user = await user_service.get_user_active(user_id=user_id)
     user_in = UserUpdate(**jsonable_encoder(user))
     if password is not None:
          user_in.password = password
     if is_active is not None:
          user_in.is_active = is_active
     if firstname is not None:
          user_in.firstname = firstname
     if lastname is not None:
          user_in.lastname = lastname
     user = await user_service.update_user(db_user=user, serialized_user=user_in)
     return UserBase(**jsonable_encoder(user))


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(user_id: int, session: AsyncSession= Depends(get_db)):
     if not user_id:
          raise 
     await  UserService(session=session).delete_user(user_id=user_id)