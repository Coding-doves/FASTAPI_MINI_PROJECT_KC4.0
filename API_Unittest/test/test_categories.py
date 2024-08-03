import unittest
from fastapi.testclient import TestClient
from app.main import app  # Import your FastAPI app
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

class TestCategory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)
    
    def test_create_category(self):
        response = client.post("/shop/category", json={"name": "New Category 1"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "New Category 1")
    
    def test_read_cat_list(self):
        # Create a category first
        client.post("/shop/category", json={"name": "New Categoryy 2"})
        
        response = client.get("/shop/cat_list/")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_read_cat(self):
        # Create a category first
        create_response = client.post("/shop/category", json={"name": "New Categoryy 4"})
        category_id = create_response.json()["id"]
        
        response = client.get(f"/shop/category/{category_id}/")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "New Categoryy 4")

    def test_update_cat(self):
        # Create a category first
        create_response = client.post("/shop/category", json={"name": "Category to Updatee"})
        category_id = create_response.json()["id"]
        
        response = client.put(f"/shop/category/{category_id}", json={"name": "Updated Categoryy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Categoryy")

    def test_delete_cat(self):
        # Create a category first
        create_response = client.post("/shop/category", json={"name": "Category to Delete"})
        category_id = create_response.json()["id"]
        
        response = client.delete(f"/shop/category/{category_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Category to Delete")

        
if __name__ == "__main__":
    unittest.main()
