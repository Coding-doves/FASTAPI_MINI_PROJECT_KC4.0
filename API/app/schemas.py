from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    username:str
    firstname:str
    lastname:str


class CreateUser(UserBase):
    passwd:str


class User(UserBase):
    id:int
    active:bool

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str
