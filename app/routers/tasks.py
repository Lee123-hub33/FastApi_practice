from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# 1. CREATE a new task (POST endpoint)
@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Unpack Pydantic data directly into the SQLAlchemy model
    new_task = models.Task(**task_data.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # Reloads tracking records directly from PostgreSQL
    return new_task


# 2. GET all tasks (with pagination and dual-sorting)
@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
        skip: int = 0,
        limit: int = 10,
        completed: bool = None,
        db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if completed is not None:
        query = query.filter(models.Task.is_completed == completed)

    # ✨ FIXED: Sort by newest created_at first, and use id descending as a tie-breaker
    tasks = query.order_by(
        models.Task.created_at.desc(),
        models.Task.id.desc()
    ).offset(skip).limit(limit).all()

    return tasks


# 3. UPDATE a task's status to completed (PATCH endpoint)
@router.patch("/{task_id}/complete", response_model=schemas.TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_completed = True

    db.commit()
    db.refresh(task)
    return task