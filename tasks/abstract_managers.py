from abc import ABC, abstractmethod
from typing import List

from tasks.models import CreateTask, ReadTask, UpdateTask


class AbstractTaskManager(ABC):
    @abstractmethod
    def create_task(self, user_id: str, task: CreateTask) -> ReadTask:
        pass

    @abstractmethod
    def update_task(self, id: str, task_data: UpdateTask) -> ReadTask:
        pass

    @abstractmethod
    def get_task_by_id(self, id: str) -> ReadTask:
        pass

    @abstractmethod
    def get_task_list(self) -> List[ReadTask]:
        pass

    @abstractmethod
    def get_user_tasks(self, user_id: str) -> List[ReadTask]:
        pass

    @abstractmethod
    def delete_task(self, id: str) -> bool:
        pass

    @abstractmethod
    def get_uncompleted_user_tasks(self, user_id: str) -> List[ReadTask]:
        pass

    @abstractmethod
    def get_uncompleted_all_user_tasks(self) -> List[ReadTask]:
        pass

    @abstractmethod
    def get_task_analytics(self):
        pass
