from fastapi import FastAPI
from app.db import engine, metadata
from app import model
from app.Router import auth


app = FastAPI()
model.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.get("/")
def home():
    return {"Home": "Update your awareness with us"}
