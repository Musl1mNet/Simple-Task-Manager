from abc import ABC, abstractmethod
from typing import List, Optional

from users.models import ReadUser, CreateUser, UpdateUser


class AbstractUserManager(ABC):
    @abstractmethod
    def create_user(self, user: CreateUser) -> ReadUser:
        """Create a new user and return the created user."""
        pass

    @abstractmethod
    def update_user(self, id: str, user_data: UpdateUser) -> ReadUser:
        """Update an existing user by ID and return the updated user."""
        pass

    @abstractmethod
    def get_user_by_id(self, id: str) -> ReadUser:
        """Retrieve a user by ID."""
        pass

    @abstractmethod
    def get_user_list(self) -> List[ReadUser]:
        """Retrieve a list of users."""
        pass

    @abstractmethod
    def search_by_email(self, email: str) -> Optional[ReadUser]:
        """Search for a user by email."""
        pass

    @abstractmethod
    def delete_user(self, id: str) -> bool:
        """Delete a user by ID. Return True if successful, False otherwise."""
        pass
