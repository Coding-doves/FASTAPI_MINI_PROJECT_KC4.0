from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, List

router = APIRouter()

class Book(BaseModel):
    id: str
    title: str
    author: str
    publication: str
    year: int
    genre: str

class BookCollection:
    def __init__(self):
        self.books: Dict[str, Book] = {}

    def new_book(self, bk: Book):
        if bk.id in self.books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book with this ID exists")
        self.books[bk.id] = bk

    def retrieve_a_book(self, bk_id: str) -> Book:
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exist")
        return self.books[bk_id]

    def retrieve_all_book(self) -> List[Book]:
        return list(self.books.values())

    def update_book(self, bk_id: str, upd_details: Book):
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exist")
        self.books[bk_id] = upd_details
        return upd_details

    def delete_book(self, bk_id: str) -> Book:
        if bk_id not in self.books:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book with this ID does not exist")
        return self.books.pop(bk_id)

book_coll = BookCollection()

@router.post("/books/", response_model=Book)
def add_new_book(book: Book):
    book_coll.new_book(book)
    return book

@router.get("/all_books/", response_model=List[Book])
def retrieve_all_books():
    return book_coll.retrieve_all_book()

@router.get("/one_book/{bk_id}", response_model=Book)
def retrieve_a_book(bk_id: str):
    return book_coll.retrieve_a_book(bk_id)

@router.put("/edit_book/{bk_id}", response_model=Book)
def update_a_book(bk_id: str, bk: Book):
    return book_coll.update_book(bk_id, bk)

@router.delete("/del_book/{bk_id}", response_model=Book)
def delete_a_book(bk_id: str):
    return book_coll.delete_book(bk_id)
