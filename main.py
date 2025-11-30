# app/main.py
from fastapi import FastAPI

from db.session import engine
from db.databases import Base
import models
from routers import users, auth, tasks

app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

# include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
