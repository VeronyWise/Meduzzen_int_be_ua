from fastapi import FastAPI
import sqlalchemy
from app.db import database
from app.routers.routers import user_router


app = FastAPI(debug=True)
metadata = sqlalchemy.MetaData()

app.include_router(router=user_router)

@app.on_event("startup")
async def startup():
    # when the application starts, we establish a connection to the database
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    # when the application stops, disconnect the connection to the database
    await database.disconnect()



@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}