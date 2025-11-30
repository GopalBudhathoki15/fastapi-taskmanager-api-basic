from fastapi import FastAPI, Depends, HTTPException, status
from databases import get_db
from schemas import (
    TaskOut,
    TaskUpdate,
    TaskCreate,
    UserBase,
    UserCreate,
    UserOut,
    UserLogin,
)
from sqlalchemy.orm import Session
import models
from security import get_password_hash


from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from security import verify_password, create_access_token
from schemas import Token


app = FastAPI()


@app.get("/users/{user_id}/tasks", response_model=list[TaskOut])
def list_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()

    return tasks


@app.post(
    "/users/{user_id}/tasks",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
)
def create_task(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(user_id=user_id, **task.model_dump())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@app.put("/users/{user_id}/tasks/{task_id}", response_model=TaskOut)
def update_task(
    user_id: int, task_id: int, task: TaskCreate, db: Session = Depends(get_db)
):
    db_task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.user_id == user_id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    db_task.title = task.title
    db_task.description = task.description
    db_task.is_completed = task.is_completed

    db.commit()
    db.refresh(db_task)

    return db_task


@app.patch("/users/{user_id}/tasks/{task_id}", response_model=TaskOut)
def patch_task(
    user_id: int, task_id: int, task: TaskUpdate, db: Session = Depends(get_db)
):
    db_task = (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id, models.Task.id == task_id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found."
        )

    update_data = task.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task


@app.delete("/users/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(user_id: int, task_id: int, db: Session = Depends(get_db)):
    db_task = (
        db.query(models.Task)
        .filter(models.Task.user_id == user_id, models.Task.id == task_id)
        .first()
    )

    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    db.delete(db_task)
    db.commit()

    return None


@app.post(
    "/users",
    tags=["users"],
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.email == user.email) | (models.User.username == user.username)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already in use.",
        )

    # hash password
    hashed_password = get_password_hash(user.password)

    # create the user model instance
    db_user = models.User(
        username=user.username, email=user.email, passsword=hashed_password
    )

    # save to db
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
