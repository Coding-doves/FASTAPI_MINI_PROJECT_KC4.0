import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestBookCollectionAPI(unittest.TestCase):
    def setUp(self):
        """Set up a test client and a new BookCollection instance before each test."""
        self.client = TestClient(app)
        self.book_coll = BookCollection()
        app.book_coll = self.book_coll  

    def test_add_new_book(self):
        """Test adding a new book to the collection."""
        response = self.client.post("/books/", json={
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })

    def test_retrieve_all_books(self):
        """Test retrieving all books from the collection."""
        self.client.post("/books/", json={
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })
        response = self.client.get("/all_books/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_retrieve_a_book(self):
        """Test retrieving a specific book by its ID."""
        self.client.post("/books/", json={
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })
        response = self.client.get("/one_book/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })

    def test_update_a_book(self):
        """Test updating a book's details."""
        self.client.post("/books/", json={
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })
        response = self.client.put("/edit_book/1", json={
            "id": "1",
            "title": "Updated Title",
            "author": "Updated Author",
            "publication": "Updated Publisher",
            "year": 2025,
            "genre": "Non-Fiction"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": "1",
            "title": "Updated Title",
            "author": "Updated Author",
            "publication": "Updated Publisher",
            "year": 2025,
            "genre": "Non-Fiction"
        })

    def test_delete_a_book(self):
        """Test deleting a book by its ID."""
        self.client.post("/books/", json={
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })
        response = self.client.delete("/del_book/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": "1",
            "title": "Book Title",
            "author": "Author Name",
            "publication": "Publisher",
            "year": 2024,
            "genre": "Fiction"
        })

    def test_retrieve_a_book_not_found(self):
        """Test retrieving a book that does not exist."""
        response = self.client.get("/one_book/999")
        self.assertEqual(response.status_code, 404)

    def test_update_a_book_not_found(self):
        """Test updating a book that does not exist."""
        response = self.client.put("/edit_book/999", json={
            "id": "999",
            "title": "Non-existent Book",
            "author": "No Author",
            "publication": "No Publisher",
            "year": 2000,
            "genre": "Unknown"
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_a_book_not_found(self):
        """Test deleting a book that does not exist."""
        response = self.client.delete("/del_book/999")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
