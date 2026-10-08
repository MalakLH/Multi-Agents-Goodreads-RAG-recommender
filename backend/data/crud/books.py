from backend.data.models.book import Book
from backend.data.schemas.book import BookCreate, BookResponse
from sqlalchemy.orm import Session

def create_book(db: Session, book: BookCreate) -> BookResponse:
    db_book = Book(**book.model_dump())

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def get_book_by_title(db: Session, title: str):
    return (
        db.query(Book)
        .filter(Book.title.ilike(title))
        .first()
    )