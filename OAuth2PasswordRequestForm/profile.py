from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import List, Dict
from uuid import uuid4


app = FastAPI()
oauth = OAuth2PasswordBearer(tokenUrl="token")

# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory storage
user_db ={}

class User(BaseModel):
    username: str
    full_name: str = None
    hashed_password:str


class UserInDB(User):
    hashed_password: str


class UserProfile(BaseModel):
    username: str
    full_name: str = None
