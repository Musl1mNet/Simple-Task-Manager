from typing import List, Optional
from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    regular = "Regular"
    admin = "Admin"


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.regular


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None


class ReadUser(CreateUser):
    id: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
