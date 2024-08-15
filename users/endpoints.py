from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from users.auth import create_access_token
from users.managers import UserManager
from .models import CreateUser, ReadUser, Token, UserLogin
from elasticsearch import Elasticsearch
from config.settings import Settings
router = APIRouter()
settings = Settings()
es = Elasticsearch(hosts=[settings.es_host,])
user_manager = UserManager()


@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user_manager.search_by_email(form_data.username)
    if not user or not user_manager.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=ReadUser)
async def register(user: CreateUser):
    email_exists = user_manager.search_by_email(user.email)
    if email_exists is not None:
        raise HTTPException(status_code=400, detail="Email already registered")

    created_user = user_manager.create_user(user)
    return created_user
