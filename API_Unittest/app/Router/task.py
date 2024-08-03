from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app import db 
from app import model, schemas

router = APIRouter()


@router.post("/tasks/{user_id}", response_model=schemas.Task)
def create_task(user_id: int, task: schemas.TaskBase, db: Session = Depends(db.get_db("task"))):
    db_task = model.Task(
        title = task.title,
        description = task.description,
        owner_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.get("/tasks/", response_model=list[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db("task"))):
    return db.query(model.Task).offset(skip).limit(limit).all()

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.TaskBase, db: Session = Depends(db.get_db("task"))):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@router.delete("/task/{task_id}", response_model=schemas.Task)
def delete_post(task_id: int, db: Session = Depends(db.get_db("task"))):
    db_task = db.query(model.Task).filter(model.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return db_task

