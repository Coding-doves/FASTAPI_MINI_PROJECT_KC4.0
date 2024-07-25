from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
class ChooseDB:
    def __init__(self):
        self.auth_db_url = "sqlite:///./auth.db"
        self.blog_db_url = "sqlite:///./blog.db"
        self.task_db_url = "sqlite:///./task.db"
        self.shop_db_url = "sqlite:///./shop.db"

    def get_engine(self, db_name):
        db_url = getattr(self, f"{db_name}_db_url")
        return create_engine(db_url, connect_args={"check_same_thread": False})
    
    def get_session_local(self, db_name):
        engine = self.get_engine(db_name)
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global instance
db_chooser = ChooseDB()
