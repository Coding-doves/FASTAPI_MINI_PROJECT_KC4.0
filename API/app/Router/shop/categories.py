from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import model, schemas, dependencies
from app import db 

router = APIRouter()


@router.post("/category", response_model=schemas.Category)
def create_category(section: schemas.CategoryBase, db:Session = Depends(db.get_db("shop"))):
    db_cat = model.Category(name = section.name)
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/cat_list/", response_model=list[schemas.Category])
def read_cat_list(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("shop"))):
    return db.query(model.Category).offset(skip).limit(limit).all()

@router.get("/category/{id}/", response_model=schemas.Category)
def read_cat(id: int, db: Session = Depends(db.get_db("shop"))):
    db_cat = db.query(model.Category).filter(model.Category.id == id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_cat

@router.put("/category/{id}", response_model=schemas.Category)
def update_cat(id: int, cat: schemas.CategoryBase, db: Session = Depends(db.get_db("shop"))):
    db_cat = db.query(model.Category).filter(model.Category.id == id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in cat.dict().items():
        setattr(db_cat, key, value)

    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)

    return db_cat

@router.delete("/category/{id}", response_model=schemas.Category)
def delete_cat(id: int, db: Session = Depends(db.get_db("shop"))):
    db_cat = db.query(model.Category).filter(model.Category.id == id).first()
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_cat)
    db.commit()
    return db_cat
