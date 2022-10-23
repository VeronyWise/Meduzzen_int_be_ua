from string import hexdigits
from db import database
from app.server.models import User, users
import schemas
from hashlib import sha256


async def get_user(user_id: int) -> int:
     user = dict(await database.fetch_one(users.select().where(users.c.id==user_id)))
     return user

async def get_user_by_email(email: str) -> str:
     return await database.fetch_one(users.select().where(users.c.email==email))

async def get_users(skip: int=0, limit: int=100):
     results = await database.fetch_all(users.select().offset(skip).limit(limit))
     return [dict(result) for result in results]

async def create_user(user: schemas.UserCreate):
     # hash the password - user.password
     fake_hashed_password = sha256(user.password.encode('utf-8')).hexdigest()
     db_user = users.insert().values(email=user.email, hashed_password=fake_hashed_password)
     user_id = await database.execute(db_user)
     return schemas.User(**user.dict(), id=user_id)

async def update_user(serialised_user: schemas.UserUpdate, curent_user: users):
     query = curent_user.update().values(**serialised_user.dict())
     user_id = await database.execute(query)
     return schemas.User(**serialised_user.dict(), id=user_id)

async def delete_user(curent_user: users):
     query = curent_user.delete()
     return await database.execute(query)

