from backend.data.models.shelf_book import ShelfBook


def prepare_shelf_for_profiler(
    shelf_books: list[ShelfBook]
) -> list[dict]:

    prepared_books = []

    for book in shelf_books:

        # Normalize personal ratings
        user_rating = book.user_rating

        if user_rating is not None:
            if user_rating <= 0 or user_rating > 5:
                user_rating = None

        # Convert database records into dictionaries
        prepared_books.append({
            "shelf_book_id": book.id,
            "title": book.title,
            "author": book.author,
            "user_rating": user_rating,
            "avg_rating": book.avg_rating,
            "date_added": (
                book.date_added.isoformat()
                if book.date_added
                else None
            )
        })

    return prepared_books