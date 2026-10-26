# project/starter/app/routers/tasks.py
# Module 5 Project — Task endpoints (auth-scoped)
#
# TODO: Implement full task CRUD, all endpoints protected by get_current_user
# All queries must filter by current_user.id (users can only see their own tasks)

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.schemas.task import TaskCreate, TaskPatch, TaskResponse
from app.database import get_db
from app.models.task import Task
from app.auth import get_current_user
from app.models.user import User

from typing import Optional
from fastapi import Query
from app.models.task import TaskPriority
from app.utils.exceptions import NotFoundException



router = APIRouter()


# TODO: POST /tasks

def log_task_creation(task_id: int, user_id: int):
    print(f"BACKGROUND LOG: User {user_id} created task {task_id}")

@router.post("/", response_model=TaskResponse, status_code=201)

def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):


    """Create a new task."""
    db_task = Task(**task.model_dump(), owner_id=current_user.id)
    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        background_tasks.add_task(
            log_task_creation,
            db_task.id,
            current_user.id
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Task could not be created due to a database constraint conflict."
    )
    return db_task


# TODO: GET /tasks

@router.get("/", response_model=list[TaskResponse])

def list_tasks(
    completed: Optional[bool] = None,
    priority: Optional[TaskPriority] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Task).filter(Task.owner_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    tasks = query.offset(skip).limit(limit).all()

    return tasks

# TODO: GET /tasks/{task_id}

@router.get("/{task_id}", response_model=TaskResponse)

def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()

    if not task:
        raise NotFoundException("Task", task_id)

    return task

# TODO: PATCH /tasks/{task_id}

@router.patch("/{task_id}", response_model=TaskResponse)

def patch_task(
    task_id: int,
    task_data: TaskPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Partially update a task owned by the current user."""

    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(exclude_unset=True)
    print("PATCH DATA:", update_data)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    return db_task

# TODO: DELETE /tasks/{task_id}

@router.delete("/{task_id}", status_code=204)

def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    """Delete a task."""
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(db_task)
    db.commit()


# TODO: GET /tasks/{task_id}/suggest — placeholder for AI suggestion
@router.get("/{task_id}/suggest")
@router.post("/{task_id}/suggest")
def suggest_task_action(
    task_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    """
    Placeholder endpoint for AI-powered task suggestions.
    TODO: Return a mock suggestion dict.
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
    "task_id": task_id,
    "suggestion": "Break this task into smaller steps and complete the highest-priority step first."
}
