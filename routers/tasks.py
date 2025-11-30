# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.databases import get_db
from schemas.task import TaskOut, TaskUpdate, TaskCreate
from core.security import get_current_user
from models.user import User
from models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks


@router.post(
    "",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = Task(
        user_id=current_user.id,
        **task.model_dump(),
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task: TaskCreate,  # you *probably* want TaskUpdate here later
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.user_id == current_user.id,
        )
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    db_task.title = task.title
    db_task.description = task.description
    db_task.is_completed = task.is_completed

    db.commit()
    db.refresh(db_task)

    return db_task


@router.patch("/{task_id}", response_model=TaskOut)
def patch_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id,
            Task.id == task_id,
        )
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found.",
        )

    update_data = task.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_task = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id,
            Task.id == task_id,
        )
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db.delete(db_task)
    db.commit()

    return None
