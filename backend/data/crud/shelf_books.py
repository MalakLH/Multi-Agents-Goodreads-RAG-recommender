from backend.data.models.shelf_book import ShelfBook
from backend.data.schemas.shelf_book import ShelfBookCreate, ShelfBookResponse
from sqlalchemy.orm import Session

def create_shelf_book(db: Session, shelf_book: ShelfBookCreate) -> ShelfBookResponse:
    db_shelf_book = ShelfBook(**shelf_book.model_dump())

    db.add(db_shelf_book)
    db.commit()
    db.refresh(db_shelf_book)
    return db_shelf_book

def book_exist_in_shelf(db: Session, title: str):

    book= db.query(ShelfBook).filter(ShelfBook.title.ilike(title)).first()
    shelf= True

    if not book:
        shelf = False

    return shelf

