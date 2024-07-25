from pydantic import BaseModel
from typing import List

"""Task 3"""
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


"""Task 1"""

class CommentBase(BaseModel):
    content: str


class Comment(CommentBase):
    id: int
    post_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: int
    author_id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True

class AuthorBase(BaseModel):
    name: str


class Author(AuthorBase):
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True
