import unittest
from fastapi.testclient import TestClient
from app.main import app  
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import model

# Setup the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestTask(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)

    def test_create_task(self):
        user_id = 1 

        response = client.post(f"/task/tasks/{user_id}", json={"title": "New Task", "description": "Task description"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "New Task")
        self.assertEqual(response.json()["description"], "Task description")

    def test_read_tasks(self):
        # Create a task first
        user_id = 1  
        client.post(f"/task/tasks/{user_id}", json={"title": "Task for Reading", "description": "Read task"})

        response = client.get("/task/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_update_task(self):
        # Create a task first
        user_id = 1  # Assuming a user with ID 1 exists
        task_response = client.post(f"/task/tasks/{user_id}", json={"title": "Old Title", "description": "Old Description"})
        task_id = task_response.json()["id"]

        response = client.put(f"/task/tasks/{task_id}", json={"title": "Updated Title", "description": "Updated Description"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Title")
        self.assertEqual(response.json()["description"], "Updated Description")

    def test_delete_task(self):
        # Create a task first
        user_id = 1  # Assuming a user with ID 1 exists
        task_response = client.post(f"/task/tasks/{user_id}", json={"title": "Task to Delete", "description": "Delete this task"})
        task_id = task_response.json()["id"]

        response = client.delete(f"/task/task/{task_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Task to Delete")


if __name__ == "__main__":
    unittest.main()
