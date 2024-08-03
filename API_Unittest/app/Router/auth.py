from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import db 
from app import model, schemas
from app.dependencies import hash_password, verify_passwd, create_access_token, ACCESS_TOKEN_EXPIRATION
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import List 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter()


def get_role(db: Session, role_name: str):
    role = db.query(model.Roles).filter(model.Roles.name == role_name).first()
    if not role:
        role = model.Roles(name=role_name)
        db.add(role)
        db.commit()
        db.refresh(role)
    return role


@router.post("/register_user", response_model=schemas.User)
def reg(user: schemas.CreateUser, db: Session = Depends( db.get_db("auth"))):
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username exists")
    
    hashed_pwd = hash_password(user.passwd)
    db_user = model.User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        hashed_pwd=hashed_pwd
    )
    user_role = get_role(db, "user")
    db_user.roles.append(user_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return  db_user

@router.post("/register_admin", response_model=schemas.User)
def reg(user: schemas.CreateUser, db: Session = Depends(db.get_db("auth"))):
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username exists")
    
    hashed_pwd = hash_password(user.passwd)
    db_user = model.User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        hashed_pwd=hashed_pwd
        
    )
    admin_role = get_role(db, "admin")
    db_user.roles.append(admin_role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return  db_user


@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db("auth"))):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    access_token = create_access_token(
        data={"sub": user.username}, expires=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user or not verify_passwd(password, user.hashed_pwd):
        return False
    return user

# get user by id
@router.get("/users_i/{user_id}", response_model=schemas.User)
def read_user_by_id(user_id: int, db: Session = Depends(db.get_db("auth"))):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# get user by user_name
@router.get("/users_n/{user_name}", response_model=schemas.User)
def read_user_by_name(user_name: str, db: Session = Depends(db.get_db("auth"))):
    db_user = db.query(model.User).filter(model.User.username == user_name).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# get all user
@router.get("/users", response_model=List[schemas.User])
def read_user(db: Session = Depends(db.get_db("auth")), skip: int = 0, limit: int = 10):
    return  db.query(model.User).filter(model.User.username).offset(skip).limit(limit).all()
