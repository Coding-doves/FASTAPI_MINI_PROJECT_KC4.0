from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta 
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from app import model


SECRET_KEY = "blog"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = 30

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_passwd(plain_password:str, db_hashed_pwd:str) -> bool:
    return pwd_context.verify(plain_password, db_hashed_pwd)

def create_access_token(data:dict, expires:timedelta = None) -> str:
    encode = data.copy()
    if expires:
        exp = datetime.utcnow() + expires
    else:
        exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    encode.update({"exp": exp})
    encode_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt
