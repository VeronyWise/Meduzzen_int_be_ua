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












# # Create the path operation function to create notes
# @app.get("/notes/", response_model=List[Note])
# async def read_notes():
#     query = notes.select()
#     return await database.fetch_all(query)


# @app.post("/notes/", response_model=Note)
# async def create_note(note: NoteIn):
#     query = notes.insert().values(text=note.text, completed=note.completed)
#     last_record_id = await database.execute(query)
#     return {**note.dict(), "id": last_record_id}










@app.get('/')
def root():
     return {'status': "Working"}

@app.get('/healthcheck')
def healthy_condition():
    return {'status': "Working"}