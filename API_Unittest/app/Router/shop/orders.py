from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import model, schemas, dependencies
from app import db 

router = APIRouter()

@router.post("/create_order", response_model=schemas.Order)
def create_order(product: schemas.OrderBase, db:Session = Depends(db.get_db("shop"))):
    db_order = model.Order(
        product_id = product.product_id,
        customer_id = product.customer_id,
        quantity = product.quantity,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/order_list/", response_model=list[schemas.Order])
def read_order_list(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("shop"))):
    return db.query(model.Order).offset(skip).limit(limit).all()

@router.get("/order/{id}/", response_model=schemas.Order)
def read_order(id: int, db: Session = Depends(db.get_db("shop"))):
    db_order = db.query(model.Order).filter(model.Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/order/{id}", response_model=schemas.Order)
def update_order(id: int, product: schemas.OrderBase, db: Session = Depends(db.get_db("shop"))):
    db_order = db.query(model.Order).filter(model.Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict().items():
        setattr(db_order, key, value)

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order

@router.delete("/order/{id}", response_model=schemas.Order)
def delete_order(id: int, db: Session = Depends(db.get_db("shop"))):
    db_order = db.query(model.Order).filter(model.Order.id == id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(db_order)
    db.commit()
    return db_order

