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

class TestPost(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create the database tables
        model.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        # Drop the database tables
        model.Base.metadata.drop_all(bind=engine)

def test_create_author():
    response = client.post("/blog/authors/", json={"name": "Author Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Author Name"
'''
def test_read_authors():
    # First create an author
    client.post("/blog/authors/", json={"name": "Author Name"})
    response = client.get("/blog/authors/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_post():
    # Create an author first
    author_response = client.post("/blog/authors/", json={"name": "Author Name"})
    author_id = author_response.json()["id"]
    
    response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": author_id})
    assert response.status_code == 200
    assert response.json()["title"] == "Post Title"

def test_read_posts():
    # Create a post first
    client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    response = client.get("/blog/posts/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_post():
    # Create a post first
    post_response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    post_id = post_response.json()["id"]
    
    response = client.get(f"/blog/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Post Title"

def test_update_post():
    # Create a post first
    post_response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    post_id = post_response.json()["id"]
    
    response = client.put(f"/blog/posts/{post_id}", json={"title": "Updated Title", "content": "Updated Content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_post():
    # Create a post first
    post_response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    post_id = post_response.json()["id"]
    
    response = client.delete(f"/blog/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Post Title"

def test_comment_post():
    # Create a post first
    post_response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    post_id = post_response.json()["id"]
    
    response = client.post(f"/blog/posts/{post_id}/comments/", json={"content": "Comment Content"})
    assert response.status_code == 200
    assert response.json()["content"] == "Comment Content"

def test_read_comments():
    # Create a comment first
    post_response = client.post("/blog/posts/", json={"title": "Post Title", "content": "Post Content"}, params={"author_id": 1})
    post_id = post_response.json()["id"]
    client.post(f"/blog/posts/{post_id}/comments/", json={"content": "Comment Content"})
    
    response = client.get("/comments/")
    assert response.status_code == 200
    assert len(response.json()) > 0
'''

if __name__ == "__main__":
    unittest.main()
