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

class TestProduct(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)

    def setUp(self):
        pass

    def tearDown(self):
        # Clean up data from the database to ensure tests start fresh
        db = TestingSessionLocal()
        db.query(model.Product).delete()
        db.commit()
        db.close()
    
    def test_create_product(self):
        response = client.post("/shop/create_product", json={
            "name": "New Product",
            "description": "Product Description",
            "price": 100.0,
            "category_id": 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "New Product")
    
    def test_read_prod_list(self):
        # Create a product first
        client.post("/shop/create_product", json={
            "name": "Product for Listing",
            "description": "Description",
            "price": 150.0,
            "category_id": 1
        })
        
        response = client.get("/shop/products_list/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_read_product(self):
        # Create a product first
        create_response = client.post("/shop/create_product", json={
            "name": "Product for Read",
            "description": "Description",
            "price": 200.0,
            "category_id": 1
        })
        product_id = create_response.json()["id"]
        
        response = client.get(f"/shop/product/{product_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Product for Read")

    def test_update_product(self):
        # Create a product first
        create_response = client.post("/shop/create_product", json={
            "name": "Product to Update",
            "description": "Description",
            "price": 250.0,
            "category_id": 1
        })
        product_id = create_response.json()["id"]
        
        response = client.put(f"/shop/product_update/{product_id}", json={
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 300.0,
            "category_id": 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated Product")

    def test_delete_product(self):
        # Create a product first
        create_response = client.post("/shop/create_product", json={
            "name": "Product to Delete",
            "description": "Description",
            "price": 350.0,
            "category_id": 1
        })
        product_id = create_response.json()["id"]
        
        response = client.delete(f"/shop/product/{product_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Product to Delete")


if __name__ == "__main__":
    unittest.main()
