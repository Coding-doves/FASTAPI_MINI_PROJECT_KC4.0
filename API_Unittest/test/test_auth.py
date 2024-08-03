import unittest
from fastapi.testclient import TestClient
from app.main import app  # Update with your FastAPI app import
from app import model, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db

# Database setup for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Override the dependency to use the test database
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestPost(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)
    
    def test_register_user(self):
        response = client.post("/auth/register_user", json={
            "username": "tuser1",
            "firstname": "Test",
            "lastname": "User",
            "passwd": "testpassword"
        })
        # Print response details for debugging
        #print("Response status code:", response.status_code)
        #print("Response content:", response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())
        self.assertEqual(response.json()["username"], "tuser1")

    def test_register_admin(self):
        response = client.post("/auth/register_admin", json={
            "username": "tadmin1",
            "firstname": "Test",
            "lastname": "Admin",
            "passwd": "adminpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.json())
        self.assertEqual(response.json()["username"], "tadmin1")

    def test_login_for_access_token(self):
        # First register a user
        client.post("/auth/register_user", json={
            "username": "tlogin1",
            "firstname": "Test",
            "lastname": "Login",
            "passwd": "loginpassword"
        })

        response = client.post("/auth/login", data={
            "username": "tlogin1",
            "password": "loginpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")
    
    def test_read_user_by_id(self):
        # Register a user
        response = client.post("/auth/register_user", json={
            "username": "userbyid2",
            "firstname": "Test",
            "lastname": "User",
            "passwd": "passwordbyid"
        })
        #print(response.json()) 
        assert response.status_code == 200

        self.assertIn("id", response.json())

    def test_read_user_by_name(self):
        # First register a user
        client.post("/auth/register_user", json={
            "username": "userbyname",
            "firstname": "Test",
            "lastname": "User",
            "passwd": "passwordbyname"
        })

        response = client.get("/auth/users_n/userbyname")
        #print(response.json()) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "userbyname")
    
    def test_read_all_users(self):
        # First register a user
        client.post("/auth/register_user", json={
            "username": "testalluser",
            "firstname": "Test",
            "lastname": "User",
            "passwd": "passwordall"
        })

        response = client.get("/auth/users")
        print(response.json()) 
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
