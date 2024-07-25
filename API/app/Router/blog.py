from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import db 
from app import model, schemas
from datetime import datetime, timedelta
from typing import List


router = APIRouter()


@router.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.Author, db: Session = Depends(db.get_db("blog"))):
    db_author = model.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("blog"))):
    authors = db.query(model.Author).offset(skip).limit(limit).all()
    return authors

@router.post("/posts/", response_model=schemas.Post)
def create_post(post: schemas.Post, author_id:int, db: Session = Depends(db.get_db("blog"))):
    author_posts = post.dict()
    author_posts["author_id"] = author_id
    db_post = model.Post(**author_posts)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
