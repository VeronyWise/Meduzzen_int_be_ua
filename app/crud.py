from db import database
from app.server.models import User, users
import schemas

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
     fake_hashed_password = user.password
     db_user = users.insert().values(email=user.email, hashed_password=fake_hashed_password)
     user_id = await database.execute(db_user)
     return schemas.User(**user.dict(), id=user_id)


