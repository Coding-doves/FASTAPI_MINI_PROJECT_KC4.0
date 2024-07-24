from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db import get_db 
from app import model, schemas
from app.dependencies import hash_password, verify_passwd, create_access_token, ACCESS_TOKEN_EXPIRATION
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta 


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
def reg(user: schemas.CreateUser, db: Session = Depends(get_db)):
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
def reg(user: schemas.CreateUser, db: Session = Depends(get_db)):
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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
