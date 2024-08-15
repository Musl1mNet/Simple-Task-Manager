from fastapi import FastAPI
from users import endpoints as usr_endpoints
from tasks import endpoints as task_endpoints

app = FastAPI()

app.include_router(usr_endpoints.router, prefix="/users", tags=["users"])
app.include_router(task_endpoints.router, prefix="/tasks", tags=["tasks"])
