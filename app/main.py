from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def root():
     return {'status': "Working"}

@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}