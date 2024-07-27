from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import model, schemas, dependencies
from app import db 

router = APIRouter()

@router.post("/customer", response_model=schemas.Customer)
def create_customer(cus: schemas.CustomerBase, db:Session = Depends(db.get_db("shop"))):
    try:
        db_cus = model.Customer(
        name = cus.name,
        email = cus.email,
        )
        db.add(db_cus)
        db.commit()
        db.refresh(db_cus)
        return db_cus
    except Exception as e:
        return e

@router.get("/customer/", response_model=list[schemas.Customer])
def read_cust_list(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("shop"))):
    return db.query(model.Customer).offset(skip).limit(limit).all()

@router.get("/customer/{id}/", response_model=schemas.Customer)
def read_cust(id: int, db: Session = Depends(db.get_db("shop"))):
    db_cust = db.query(model.Customer).filter(model.Customer.id == id).first()
    if db_cust is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_cust

@router.put("/customer/{id}", response_model=schemas.Customer)
def update_cust(id: int, cust: schemas.CustomerBase, db: Session = Depends(db.get_db("shop"))):
    db_cust = db.query(model.Customer).filter(model.Customer.id == id).first()
    if db_cust is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in cust.dict().items():
        setattr(db_cust, key, value)

    db.add(db_cust)
    db.commit()
    db.refresh(db_cust)

    return db_cust

@router.delete("/customer/{id}", response_model=schemas.Customer)
def delete_cust(id: int, db: Session = Depends(db.get_db("shop"))):
    db_cust = db.query(model.Customer).filter(model.Customer.id == id).first()
    if db_cust is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_cust)
    db.commit()
    return db_cust

