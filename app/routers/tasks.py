from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# 1. CREATE a new task (This is your POST endpoint!)
@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Unpack Pydantic data directly into the SQLAlchemy model
    new_task = models.Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # Grabs the auto-generated ID and created_at timestamp
    return new_task
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks


# 3. UPDATE a task's status to completed
@router.patch("/{task_id}/complete", response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    # Look for the task by its ID
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    # If the task doesn't exist, throw a 404 error
    if not task:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Task not found")

    # Switch the status to True!
    task.is_completed = True

    db.commit()  # Save changes to PostgreSQL
    db.refresh(task)  # Grab the updated object
    return task