from fastapi import FastAPI, Depends
import sqlalchemy
# from app.db import database
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.routers.company import company_router
from app.routers.statements import statements_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer


app = FastAPI(debug=True, title="REST API using FastAPI PostgreSQL Async EndPoints")
metadata = sqlalchemy.MetaData()

app.include_router(router=user_router, tags=["Users"])
app.include_router(router=auth_router, tags=["Login"])
app.include_router(router=company_router, tags=["Company"])
app.include_router(router=statements_router, tags=["Join Statements"])


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# added Autorise buttom in swagger
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}