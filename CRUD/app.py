from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List
"""CRUD:
        Create, Read, Update, Delete
"""

app = FastAPI()


class Book(BaseModel):
    id: str
    title: str
    author: str
    publication: str
    year: int
    genre: str


class BookCollection:
    """
    Desc:
        Collection of Books.
        Handle CRUD operations
    """

    def __init__(self):
        """ intializing the BookCollection with an empty dictionary """
        self.books: Dict[str, Book] = {}

    def new_book(self, bk: Book):
        """ add new books to collection """
        if bk.id in self.books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ID exists")
        self.books[bk.id] = bk

    def retrieve_a_book(self, bk_id: str) -> Book:
        # Return a requested book
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exists")
        return self.books[bk_id]

    def retrieve_all_book(self) -> List[Book]:
        # Return a requested book
        return list(self.books.values())

    def update_book(self, bk_id: str, upd_details: Book):
        """Update book details of a book by its ID"""
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exists")
        self.books[bk_id] = upd_details
        return upd_details

    def delete_book(self, bk_id: str) -> Book:
        """Delete requested book"""
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exists")
        return self.books.pop(bk_id)


#creating book object
book_coll = BookCollection()


@app.post("/books/", response_model=Book)
def add_new_book(book:Book):
    """
    Desc:
        Add new book to collection
        response_model: verifies with Book class
                before passing to BookCollection
    param:
        book -> type of Book class
    Returns: Book class type
    """
    book_coll.new_book(book)
    return book

@app.get("/all_books/", response_model=List[Book])
def retrieve_all_books():
    """
    Desc:
        Retrieve all book in collection
    Returns: List of Books 
    """
    return book_coll.retrieve_all_book()

@app.get("/one_book/{bk_id}", response_model=Book)
def retrieve_a_books(bk_id: str):
    """
    Desc: Retrieve specific book in collection
    param: bk_id
    Returns: Book
    """
    return book_coll.retrieve_a_book(bk_id)

@app.put("/edit_book/{bk_id}", response_model=Book)
def update_a_book(bk_id:str, bk:Book):
    """
    Desc: Add new details to a book in collection
    param: bk_id, bk_details
    Returns: Book
    """
    return book_coll.update_book(bk_id, bk)

@app.delete("/del_book/{bk_id}", response_model=Book)
def delete_a_books(bk_id:str):
    """
    Desc: Delete a book in collection
    param:
    Returns: None
    """
    return book_coll.delete_book(bk_id)
