from fastapi import FastAPI
import sqlalchemy
from app.db import database
from app.routers.routers import user_router


app = FastAPI(debug=True)
metadata = sqlalchemy.MetaData()

app.include_router(router=user_router)




@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}