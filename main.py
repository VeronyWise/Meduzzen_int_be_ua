from fastapi_health import health
from fastapi import FastAPI, status


app = FastAPI()

@app.get('/')
def root():
     return {'status': "Working"}

@app.get('/healthcheck', status_code=status.HTTP_200_OK)
def healthy_condition():
    return {'status': "Working"}