from typing import List
from fastapi import APIRouter, Depends, HTTPException
from tasks.managers import TaskManager
from slowapi import Limiter
from slowapi.util import get_remote_address
from users.auth import admin_access, get_current_user
from users.models import ReadUser, Role
from .models import CreateTask, ReadTask, UpdateTask
router = APIRouter()
task_manager = TaskManager()
limiter = Limiter(key_func=get_remote_address)


@router.post("/user/tasks", response_model=ReadTask)
async def create_task(task: CreateTask, current_user: ReadUser = Depends(get_current_user)):
    created_task = task_manager.create_task(current_user.id, task)
    return created_task


@router.put("/user/tasks/{task_id}", response_model=ReadTask)
async def update_task(task_id: str, task: UpdateTask, current_user: ReadUser = Depends(get_current_user)):
    current_task = task_manager.get_task_by_id(task_id)
    if not current_task or (task.user_id != current_user.id and current_user.role != Role.admin) or (task.user_id != current_user.id and current_user.role == Role.admin):
        raise HTTPException(
            status_code=404, detail="Task not found or access denied")
    updated_task = task_manager.update_task(task_id, task)
    return updated_task


@router.get("/user/tasks/{task_id}", response_model=ReadTask)
async def read_task(task_id: str, current_user: ReadUser = Depends(get_current_user)):
    task = task_manager.get_task_by_id(task_id)
    if task is None or (task.user_id != current_user.id and current_user.role != Role.admin) or (task.user_id != current_user.id and current_user.role == Role.admin):
        raise HTTPException(
            status_code=404, detail="Task not found or access denied")
    return task


@router.get("/user/tasks/", response_model=List[ReadTask])
async def get_user_tasks(current_user: ReadUser = Depends(get_current_user)):
    result = task_manager.get_user_tasks(current_user.id)
    return result


@router.delete("/user/tasks/{task_id}")
async def get_user_tasks(task_id: str, current_user: ReadUser = Depends(get_current_user)):
    task = task_manager.get_task_by_id(task_id)
    if task is None or (task.user_id != current_user.id and current_user.role != Role.admin) or current_user.role != Role.admin:
        raise HTTPException(
            status_code=404, detail="Task not found or access denied")
    result = task_manager.delete_task(task.id)
    return result


@router.get("/admin/tasks/", response_model=List[ReadTask], dependencies=[Depends(admin_access)])
async def get_all_tasks():
    result = task_manager.get_task_list()
    return result


@router.get("/admin/analytics/", dependencies=[Depends(admin_access)])
async def get_task_analytics():
    return task_manager.get_task_analytics()
