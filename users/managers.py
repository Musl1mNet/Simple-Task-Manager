import uuid
from config.settings import settings, es
import elasticsearch
from typing import List, Optional
from passlib.context import CryptContext

from .abstract_managers import AbstractUserManager
from .models import CreateUser, ReadUser, UpdateUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager(AbstractUserManager):
    def create_user(self, user: CreateUser) -> ReadUser:
        custom_id = str(uuid.uuid4())
        hashed_password = self.hash_password(user.password)
        user_data = user.dict()
        user_data.update({"id": custom_id, "password": hashed_password})
        es.index(index=settings.user_index, id=custom_id, document=user_data)
        return ReadUser(**user_data)

    def update_user(self, id: str, user_data: UpdateUser) -> ReadUser:
        if user_data.password:
            hashed_password = self.hash_password(user_data.password)
            user_data.password = hashed_password
        es.update(index=settings.user_index, id=id,
                  body={"doc": user_data.dict()})
        updated_user = es.get(index=settings.user_index, id=id)
        return ReadUser(**updated_user['_source'])

    def get_user_by_id(self, id: str) -> ReadUser:
        user = es.get(index=settings.user_index, id=id)
        return ReadUser(**user['_source'])

    def get_user_list(self) -> List[ReadUser]:
        result = es.search(index=settings.user_index, body={
                           "query": {"match_all": {}}})
        return [ReadUser(**hit['_source']) for hit in result['hits']['hits']]

    def search_by_email(self, email: str) -> Optional[ReadUser]:
        result = es.search(index=settings.user_index, body={
            "query": {
                "match": {"email": email}
            }
        })
        if result['hits']['hits']:
            return ReadUser(**result['hits']['hits'][0]['_source'])
        return None

    def delete_user(self, id: str) -> bool:
        try:
            es.delete(index=settings.user_index, id=id)
            return True
        except elasticsearch.exceptions.NotFoundError:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return pwd_context.hash(password)
