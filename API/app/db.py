from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from .choose_db import db_chooser


metadata = MetaData()
Base = declarative_base()

def get_db(db_name: str):
    def get_db_instance():
        SessionLocal = db_chooser.get_session_local(db_name)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    return get_db_instance
