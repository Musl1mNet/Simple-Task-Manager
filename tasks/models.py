from typing import Optional

from pydantic import BaseModel


class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class ReadTask(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    completed: bool
    user_id: str


class TaskAnalysis(BaseModel):
    tasks_per_user: int
    completed_tasks: float
