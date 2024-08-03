from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import model, schemas, dependencies
from app import db 

router = APIRouter()

@router.post("/create_product", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db:Session = Depends(db.get_db("shop"))):
    db_product = model.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        category_id = product.category_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products_list/", response_model=list[schemas.Product])
def read_prod_list(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("shop"))):
    return db.query(model.Product).offset(skip).limit(limit).all()

@router.get("/product/{product_id}/", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(db.get_db("shop"))):
    db_product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/product_update/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(db.get_db("shop"))):
    db_product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_product, key, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@router.delete("/product/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(db.get_db("shop"))):
    db_product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return db_product

