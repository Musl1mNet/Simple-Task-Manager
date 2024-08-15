from .settings import es, Settings
settings = Settings()

task_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "keyword"}
        }
    }
}

usr_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "email": {"type": "keyword"},
            "password": {"type": "text"},
            "role": {"type": "keyword"},
        }
    }
}
es = es.options(ignore_status=[400])

try:
    es.indices.create(index=settings.user_index, body=usr_mapping)
except Exception as e:
    print(f"Error creating user index: {e}")

try:
    es.indices.create(index=settings.task_index, body=task_mapping)
except Exception as e:
    print(f"Error creating task index: {e}")
