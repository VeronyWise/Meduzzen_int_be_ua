from fastapi import FastAPI
import sqlalchemy
from app.db import database
from . import models, schemas


app = FastAPI()
metadata = sqlalchemy.MetaData()



@app.on_event("startup")
async def startup():
    # when the application starts, we establish a connection to the database
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # when the application stops, disconnect the connection to the database
    await database.disconnect()



@app.get('/')
def root():
     return {'status': "Working"}

@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}