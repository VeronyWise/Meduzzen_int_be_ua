from fastapi import HTTPException
from requests import session
from starlette import status
from app.models.user import User
from app.schemas import user
from hashlib import sha256
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
import re
from app.crud.base_session import BaseSession
from app.models.enummodels import StatementType, UserType


class UserService(BaseSession):

     async def get_user(self, user_id: int):
          user: User = await self.session.get(User, user_id)
          if not user:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User doesnt found!')
          return user

     async def get_all_users(self) -> List[User]:
          users = await self.session.execute(select(User).where(User.is_active))
          return users.scalars().all()

     async def get_user_by_email(self, email:str):
          user = await self.session.execute(select(User).where(User.email == email))
          user: User = user.scalars().one_or_none()
          return user

     async def create_user(self, serialized_data: user.UserCreate) -> User:
          user = await self.get_user_by_email(email=serialized_data.email)
          if user:
               raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail='User with this email already register')
          if serialized_data.hashed_password:
               self.validate_password(serialized_data.hashed_password)
               serialized_data.hashed_password = self.get_password_hash(serialized_data.hashed_password)
          result = await self.session.execute(insert(User).values(**serialized_data.dict()))
          pk = result.inserted_primary_key
          return await self.get_user(user_id=pk)

     async def get_user_active(self, user_id:int):
          user = await self.get_user(user_id=user_id)
          if not user.is_active:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User isnt active")
          return user

     async def update_user(self, db_user: User, serialized_user: user.UserUpdate):
          update_data = serialized_user.dict()
          if update_data['password']:
               password = self.validate_password(update_data['password'])
               del update_data['password']
               update_data['hashed_password'] = self.get_password_hash(password)
          for field in update_data:
               if field in update_data:
                    setattr(db_user, field, update_data[field])
          self.session.add(db_user)
          await self.session.commit()
          await self.session.refresh(db_user)
          return db_user

     async def delete_user(self, user_id:int):
          user: User = await self.get_user(user_id=user_id)
          if not user:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User doesnt found!')
          await self.session.delete(user)

     @staticmethod
     def get_password_hash(password):
          return sha256(password.encode('utf-8')).hexdigest()

     @staticmethod
     def validate_password(password):
          regex = r'((?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9]).{6,40})\S$'
          result = re.findall(regex, password)
          if not result:
               raise  HTTPException(
     status_code=status.HTTP_400_BAD_REQUEST,
     detail='Password must be minimum of 6 characters, at least 1 uppercase letter,'
               '1 lowercase letter, and 1 num with no spaces.')
          return password
