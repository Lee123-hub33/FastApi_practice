from fastapi import FastAPI
from app.routers import tasks

# REMOVED: Base.metadata.create_all(bind=engine)
# Alembic handles tracking our database tables now!

app = FastAPI(title="FastApi Modular Practice API")
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"status": "Online", "message": "Hello World"}