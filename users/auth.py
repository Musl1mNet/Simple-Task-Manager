from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer
from config.settings import settings
from users.managers import UserManager
from users.models import ReadUser, Role
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

user_manager = UserManager()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = user_manager.search_by_email(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    return user


async def admin_access(current_user: ReadUser = Depends(get_current_user)):
    if current_user.role != Role.admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user
