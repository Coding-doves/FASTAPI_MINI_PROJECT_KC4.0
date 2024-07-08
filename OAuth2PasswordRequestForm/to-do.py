from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import List, Dict
from uuid import uuid4


app = FastAPI()

"""
    VERIFICATION SET-UP
"""
# OAuth2 scheme
oauth = OAuth2PasswordBearer(tokenUrl="token")

# hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory storage
user_db ={}
task_db ={}
notes_db ={}
posts_db ={}
orders_db ={}

class User(BaseModel):
    username: str
    full_name: str = None
    hashed_password:str


class UserInDB(User):
    hashed_password: str


class Task(BaseModel):
    id: int
    title: str
    content: str = None
    done: bool = False


class UserProfile(BaseModel):
    username: str
    full_name: str = None


class Note(BaseModel):
    id: str
    title: str
    content: str
    owner: str


class Post(BaseModel):
    id: str
    title: str
    content: str
    owner: str


class Order(BaseModel):
    id: str
    item_name: str
    quantity: int
    owner: str


def get_user(usr_db, usr_name:str):
    return usr_db.get(usr_name)

def verify_user(plain_pwd, hashed_pwd):
    return pwd_context.verify(plain_pwd, hashed_pwd)

def authenticate_user(usr_db, usr_name: str, pwd: str):
    user = get_user(usr_db, usr_name)

    if not user or not verify_user(pwd, user.hashed_pwd):
        return False
    return user

def get_current_user(token: str = Depends(oauth)):
    user = user_db.get(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.post("/token")
def login(data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(user_db, data.username, data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            details="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": data.username, "token_type": "bearer"}

@app.post("/register")
def register(user: User):
    if user.username in user_db:
        raise HTTPException(status_code=400, detail="Username already exist")
    hashed_pwd = pwd_context.hash(user.hashed_password)
    user_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_pwd)
    return {"msg": "User registered successfully"}

# End of VERIFICATION SET-UP


"""
    Task 1
"""
@app.post("/tasks/", response_model=Task)
def create_task(task: Task, current_user = Depends(get_current_user)):
    task_id = str(uuid4())
    task.id = task_id
    task_db[task_id] = task
    return task

@app.get("/tasks/{task_id}", response_model=List[Task])
def read_tasks(current_user: User = Depends(get_current_user)):
    return list(task_db.values())

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id:str, task: Task, current_user: User = Depends(get_current_user)):
    if task_id not in task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task_db[task_id] = task
    return task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id:str, current_user: User = Depends(get_current_user)):
    task = task_db.pop(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


"""
    Task 2
"""
@app.get("/profile", response_model=UserProfile)
def read_profile(current_user: User = Depends(get_current_user)):
    return UserProfile(**current_user.dict())

@app.put("/profile", response_model=UserProfile)
def update_profile(profile: UserProfile, current_user: User = Depends(get_current_user)):
    user_data = user_db.get(current_user.username)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    upd_user = user_data.copy(update=profile.dict())
    user_db[current_user.username] = upd_user
    return UserProfile(**upd_user.dict())


"""
    Task 3
"""
@app.post("/notes/", response_model=Note)
def create_note(note: Note, current_user: User = Depends(get_current_user)):
    note_id = str(uuid4())
    note.id = note_id
    note.owner = current_user.username
    notes_db[note_id] = note
    return note

@app.get("/notes/", response_model=List[Note])
def display_notes(current_user: User = Depends(get_current_user)):
    return [n for n in notes_db.values() if n.owner == current_user.username]

@app.get("/notes/{notes_id}", response_model=Note)
def read_note(note_id: str, current_user: User = Depends(get_current_user)):
    note = notes_db.get(note_id)
    if note is None or note.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return note

@app.put("/notes/{note_id}", response_model=Note)
def update_note(note_id: str, note: Note, current_user: User = Depends(get_current_user)):
    stored_note = notes_db.get(note_id)
    if stored_note is None or stored_note.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    note.id = note_id
    note.owner = current_user.username
    notes_db[note_id] = note
    return note

@app.delete("/notes/{note_id}", response_model=Note)
def delete_note(note_id: str, current_user: User = Depends(get_current_user)):
    note = notes_db.get(note_id)
    if note is None or note.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return notes_db.pop(note_id)


"""
    Task 4
"""
@app.post("/posts/", response_model=Post)
def create_post(post: Post, current_user: User = Depends(get_current_user)):
    post_id = str(uuid4())
    post.id = post_id
    post.owner = current_user.username
    posts_db[post_id] = post
    return post

@app.get("/posts/", response_model=List[Post])
def display_posts(current_user: User = Depends(get_current_user)):
    return [post for post in posts_db.values() if post.owner == current_user.username]

@app.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: str, current_user: User = Depends(get_current_user)):
    post = posts_db.get(post_id)
    if post is None or post.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    return post

@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: str, post: Post, current_user: User = Depends(get_current_user)):
    stored_post = posts_db.get(post_id)
    if stored_post is None or stored_post.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    post.id = post_id
    post.owner = current_user.username
    posts_db[post_id] = post
    return post

@app.delete("/posts/{post_id}", response_model=Post)
def delete_post(post_id: str, current_user: User = Depends(get_current_user)):
    post = posts_db.get(post_id)
    if post is None or post.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    return posts_db.pop(post_id)


"""
Task 5
"""
@app.get("/account", response_model=User)
def get_account_detail(current_user: User = Depends(get_current_user)):
    return current_user

@app.put("/account", response_model=User)
def update_account_detail(user: User, current_user: User = Depends(get_current_user)):
    if current_user.username not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user.hashed_password = user_db[current_user.username].hashed_password
    user_db[current_user.username] = user

    return user

@app.post("/orders/", response_model=Order)
def place_order(order: Order, current_user: User = Depends(get_current_user)):
    order_id = str(uuid4())
    order.id = order_id
    order.owner = current_user.username
    orders_db[order_id] = order

    return order

@app.get("/orders/", response_model=List[Order])
def display_order_history(current_user: User = Depends(get_current_user)):
    return [order for order in order_db.values() if order.owner == current_user.username]

@app.get("/orders/{order_id}", response_model=Order)
def view_order(order_id: str, current_user: User = Depends(get_current_user)):
    order = orders_db.get(order_id)
    if order is None or order.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return order

@app.delete("/orders/{order_id}", response_model=Order)
def delete_order(order_id:str, current_user: User = Depends(get_current_user)):
    order = orders_db.get(order_id)
    if order is None or order.owner != current_user.username:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return orders_db.pop(order_id)
