from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    is_completed: bool = False


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool | None = None


class TaskOut(TaskBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)
