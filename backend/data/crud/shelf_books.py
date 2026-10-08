from backend.data.models.shelf_book import ShelfBook
from backend.data.schemas.shelf_book import ShelfBookCreate, ShelfBookResponse
from sqlalchemy.orm import Session

def create_shelf_book(db: Session, shelf_book: ShelfBookCreate) -> ShelfBookResponse:
    db_shelf_book = ShelfBook(**shelf_book.model_dump())

    db.add(db_shelf_book)
    db.commit()
    db.refresh(db_shelf_book)
    return db_shelf_book