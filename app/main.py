from fastapi import FastAPI
from app.database import engine, Base
from app.routers import tasks
from app import models

Base.metadata.create_all(bind=engine)
app = FastAPI(tittle="FastApi Modular Practice API")
app.include_router(tasks.router)
@app.get("/")
def root():
    return {"status": "Online", "message": "Hello World"}