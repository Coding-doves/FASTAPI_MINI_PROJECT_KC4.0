from pydantic import BaseModel
from typing import List, Optional

"""Task 3"""
class UserBase(BaseModel):
    username:str
    firstname:str
    lastname:str


class CreateUser(UserBase):
    passwd:str


class User(UserBase):
    id:Optional[int]
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
    id: Optional[int]
    post_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str


class Post(PostBase):
    id: Optional[int]
    author_id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    name: str


class Author(AuthorBase):
    id: Optional[int]
    posts: List[Post] = []

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str
    description: str = None
    completed: bool = False


class Task(TaskBase):
    id: Optional[int]
    owner_id: int

    class Config:
        orm_mode = True

"""Task 2"""
class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    description: str
    price: float

class ProductCreate(ProductBase):
    category_id: int

class Product(ProductBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    name: str
    email: str

class Customer(CustomerBase):
    id: Optional[int]

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    product_id: int
    customer_id: int
    quantity: int

class Order(OrderBase):
    id: Optional[int]

    class Config:
        orm_mode = True
