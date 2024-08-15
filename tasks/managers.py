from typing import List
from config.settings import settings, es
import uuid
import elasticsearch
from tasks.abstract_managers import AbstractTaskManager
from tasks.models import CreateTask, ReadTask, TaskAnalysis, UpdateTask


class TaskManager(AbstractTaskManager):
    def create_task(self, user_id: str, task: CreateTask) -> ReadTask:
        custom_id = str(uuid.uuid4())
        task_data = task.dict()
        task_data.update({"id": custom_id, "user_id": user_id})
        es.index(index=settings.task_index, id=custom_id, document=task_data)
        return ReadTask(**task_data)

    def update_task(self, id: str, task_data: UpdateTask) -> ReadTask:
        es.update(index=settings.task_index, id=id, body={
                  "doc": task_data.dict(exclude_unset=True)})
        updated_task = es.get(index=settings.task_index, id=id)
        return ReadTask(**updated_task['_source'])

    def get_task_by_id(self, id: str) -> ReadTask:
        task = es.get(index=settings.task_index, id=id)
        return ReadTask(**task['_source'])

    def get_task_list(self) -> List[ReadTask]:
        result = es.search(index=settings.task_index, body={
                           "query": {"match_all": {}}})
        return [ReadTask(**hit['_source']) for hit in result['hits']['hits']]

    def get_user_tasks(self, user_id: str) -> List[ReadTask]:
        result = es.search(index=settings.task_index, body={
            "query": {
                "term": {"user_id": user_id}
            }
        })
        return [ReadTask(**hit['_source']) for hit in result['hits']['hits']]

    def delete_task(self, id: str) -> bool:
        try:
            es.delete(index=settings.task_index, id=id)
            return True
        except elasticsearch.exceptions.NotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def get_uncompleted_user_tasks(self, user_id: str) -> List[ReadTask]:
        result = es.search(index=settings.task_index, body={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"user_id": user_id}},
                        {"term": {"completed": False}}
                    ]
                }
            }
        })
        return [ReadTask(**hit['_source']) for hit in result['hits']['hits']]

    def get_uncompleted_all_user_tasks(self) -> List[ReadTask]:
        result = es.search(index=settings.task_index, body={
            "query": {
                "term": {"completed": False}
            }
        })
        return [ReadTask(**hit['_source']) for hit in result['hits']['hits']]

    def get_task_analytics(self):
        query = {
            "aggs": {
                "tasks_per_user": {
                    "terms": {"field": "user_id"}
                },
                "completed_tasks": {
                    "avg": {"field": "completed"}
                }
            }
        }
        result = es.search(index=settings.task_index, body=query)
        return result["aggregations"]
