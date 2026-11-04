from backend.data.models.book import Book
from backend.data.schemas.book import BookCreate, BookResponse
from sqlalchemy.orm import Session

def create_book(db: Session, book: BookCreate) -> BookResponse:

    existing_book = (
        db.query(Book)
        .filter(Book.book_url == book.book_url)
        .first()
    )

    if existing_book:
        return existing_book

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


def get_existing_book_urls(db: Session) -> set[str]:

    urls = (
        db.query(Book.book_url)
        .filter(
            Book.book_url.isnot(None),
            Book.book_url != ""
        )
        .all()
    )

    return {url[0] for url in urls}
