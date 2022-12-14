from app.crud.base_session import BaseSession
from app.crud.user import UserService
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer
from app.db.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
import jwt as auth_jwt
from app.schemas.user import UserBase, UserCreate, Token, UserLogin, UserUpdate
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from app.models.user import User
from ..settings import settings
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Dict, Optional
from app.models.user import User, Company, UserType



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')
token_auth_schema = HTTPBearer()

async def get_current_user(token =  Depends(token_auth_schema), db: AsyncSession = Depends(get_db)) -> User:
    result = VerifyToken(token.credentials).verify() 
    if 'email' in result:
        return await AuthService(db).get_or_create_user(email=result['email'])
    return await AuthService(db).verify_token(token.credentials)

async def get_owner(user = Depends(get_current_user)) -> User:
    if user.user_type != UserType.owner:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access!")
    return user

async def get_owner_or_admin(user = Depends(get_current_user)) -> User:
    if user.user_type not in (UserType.admin, UserType.owner):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access!")
    return user


exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'})

class AuthService(BaseSession):

    async def verify_token(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception
        user_id = payload.get('sub')
        user = await UserService(self.session).get_user(int(user_id))
        # return UserBase(**jsonable_encoder(user))
        return user

    @classmethod
    def create_token(cls, user: User) -> Token:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user.id),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(access_token=token)

    async def authenticate_user(self, email, password) -> Token:
        user = await UserService(self.session).get_user_by_email(email=email)
        if not user:
            raise exception
        if not self.verify_password(password=password, hashed_password=user.hashed_password):
            raise exception
        return self.create_token(user)

    async def register_new_user(self, serialized_data: UserCreate) -> Token:
        user = await UserService(self.session).create_user(serialized_data=serialized_data)
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    async def get_or_create_user(self, email) -> User:
        user_service = UserService(self.session)
        user = await user_service.get_user_by_email(email=email)
        if not user:
            user = await user_service.create_user(UserCreate(email=email))
        # return UserBase(**jsonable_encoder(user))
        return user

    @staticmethod
    def verify_password(hashed_password, password) -> bool:
        return UserService.get_password_hash(password) == hashed_password


class VerifyToken():
    def __init__(self, token):
        self.token = token

        jwks_url = f'https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json'
        self.jwks_client = auth_jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except auth_jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except auth_jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = auth_jwt.decode(
                self.token,
                self.signing_key,
                algorithms=settings.ALGORITHMS,
                audience=settings.AUTH0_API_AUDIENCE,
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return payload    