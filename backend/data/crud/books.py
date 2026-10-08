from models.book import Book
from schemas.book import BookCreate, BookResponse
from sqlalchemy.orm import Session

def create_book(db: Session, book: BookCreate) -> BookResponse:
    db_book = Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book