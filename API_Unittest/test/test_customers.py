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

class TestCustomer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)

    def setUp(self):
        # Optional: Create some initial data if necessary
        pass

    def tearDown(self):
        # Clean up data from the database to ensure tests start fresh
        db = TestingSessionLocal()
        db.query(model.Customer).delete()
        db.commit()
        db.close()

    def test_create_customer(self):
        response = client.post("/customer", json={
            "name": "John Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John Doe")
        self.assertEqual(response.json()["email"], "john.doe@example.com")

    def test_read_cust_list(self):
        # Create a customer first
        client.post("/customer", json={
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        })
        
        response = client.get("/customer/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_read_customer(self):
        # Create a customer first
        create_response = client.post("/customer", json={
            "name": "Mike Johnson",
            "email": "mike.johnson@example.com"
        })
        customer_id = create_response.json()["id"]
        
        response = client.get(f"/customer/{customer_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Mike Johnson")

    def test_update_customer(self):
        # Create a customer first
        create_response = client.post("/customer", json={
            "name": "Lisa Brown",
            "email": "lisa.brown@example.com"
        })
        customer_id = create_response.json()["id"]
        
        response = client.put(f"/customer/{customer_id}", json={
            "name": "Lisa Green",
            "email": "lisa.green@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Lisa Green")

    def test_delete_customer(self):
        # Create a customer first
        create_response = client.post("/customer", json={
            "name": "Tom Clark",
            "email": "tom.clark@example.com"
        })
        customer_id = create_response.json()["id"]
        
        response = client.delete(f"/customer/{customer_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Tom Clark")

if __name__ == "__main__":
    unittest.main()
