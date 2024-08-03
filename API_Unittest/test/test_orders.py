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

class TestOrder(unittest.TestCase):

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
        db.query(model.Order).delete()
        db.commit()
        db.close()
    
    def test_create_order(self):
        response = client.post("/shop/create_order", json={
            "product_id": 1,
            "customer_id": 1,
            "quantity": 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["product_id"], 1)
        self.assertEqual(response.json()["customer_id"], 1)
        self.assertEqual(response.json()["quantity"], 5)

    def test_read_order_list(self):
        # Create an order first
        client.post("/shop/create_order", json={
            "product_id": 1,
            "customer_id": 1,
            "quantity": 5
        })
        
        response = client.get("/shop/order_list/")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)
    
    def test_read_order(self):
        # Create an order first
        create_response = client.post("/shop/create_order", json={
            "product_id": 2,
            "customer_id": 2,
            "quantity": 10
        })
        order_id = create_response.json()["id"]
        
        response = client.get(f"/shop/order/{order_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["product_id"], 2)

    def test_update_order(self):
        # Create an order first
        create_response = client.post("/shop/create_order", json={
            "product_id": 3,
            "customer_id": 3,
            "quantity": 15
        })
        order_id = create_response.json()["id"]
        
        response = client.put(f"/shop/order/{order_id}", json={
            "product_id": 4,
            "customer_id": 4,
            "quantity": 20
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["product_id"], 4)

    def test_delete_order(self):
        # Create an order first
        create_response = client.post("/shop/create_order", json={
            "product_id": 5,
            "customer_id": 5,
            "quantity": 25
        })
        order_id = create_response.json()["id"]
        
        response = client.delete(f"/shop/order/{order_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["product_id"], 5)


if __name__ == "__main__":
    unittest.main()
