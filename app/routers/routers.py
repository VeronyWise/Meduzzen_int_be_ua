from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from fastapi import FastAPI, HTTPException
from app.db import database, engine, metadata, Session, get_db

import crud
import schemas


metadata.create_all(bind=engine)
router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/users/", response_model=schemas.UserList, status_code=status.HTTP_201_CREATED)
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
     return await crud.get_users(skip=skip, limit=limit)

@router.get("/users/{id}", response_model=schemas.UserList)
async def get_one_user(user_id: int):
     db_user = crud.get_user(user_id=id)
     if db_user is None:
          raise HTTPException(status_code=400, detail="User has not found")
     return await db_user


@router.post("/users/", response_model=schemas.UserCreate)
async def creat_user(user: schemas.UserCreate):
     db_user = await crud.get_user_by_email(email=user.email)
     if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
     return await crud.create_user(user=user)

@router.