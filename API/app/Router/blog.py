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
    db_post = model.Post(
        title=post.title,
        content=post.content,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int=0, limit:int=10, db: Session = Depends(db.get_db("blog"))):
    posts = db.query(model.Post).offset(skip).limit(limit).all()
    return posts

@router.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(db.get_db("blog"))):
    db_post = db.query(model.Post).filter(model.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post: schemas.Post, post_id:int, db: Session = Depends(db.get_db("blog"))):
    db_post = db.query(model.Post).filter(model.Post.id == post_id).first()
    
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/posts/{post_id}", response_model=schemas.Post)
def delete_post(post_id: int, db: Session = Depends(db.get_db("blog"))):
    db_post = db.query(model.Post).filter(model.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return db_post

@router.post("/posts/{post_id}/comments/", response_model=schemas.Comment)
def comment_post(comment: schemas.CommentBase, post_id:int, db: Session = Depends(db.get_db("blog"))):
    db_comment = model.Comment(
        content=comment.content,
        post_id=post_id
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment

@router.get("/comments/", response_model=List[schemas.Comment])
def read_comments(skip: int=0, limit:int=10, db: Session = Depends(db.get_db("blog"))):
    comments = db.query(model.Comment).offset(skip).limit(limit).all()
    return comments
