from backend.data.models import (
    ShelfBook,
    RecommendedBook,
    Book
)

from backend.data.db.database import SessionLocal
from backend.data.crud.shelf_books import get_all_shelf_books
from backend.data.services.shelf_book_preparation import (
    prepare_shelf_for_profiler
)


db = SessionLocal()

try:
    shelf_books = get_all_shelf_books(db)

    print(f"Retrieved {len(shelf_books)} books")

    prepared_books = prepare_shelf_for_profiler(shelf_books)

    for book in prepared_books:
        print(book)

finally:
    db.close()