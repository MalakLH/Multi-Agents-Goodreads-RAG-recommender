from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import date


from backend.data.db.database import get_db
from backend.data.crud.shelf_books import create_shelf_book
from backend.data.schemas.shelf_book import (
    ShelfBookCreate,
    ShelfBookResponse,
)
from backend.scraper.site_scraper import site_scraper


async def scrape_and_create_shelf_book(
    url: str,
    db: Session = Depends(get_db)
) -> list[ShelfBookResponse]:

    scraped_data = await site_scraper(url)

    created_books = []

    for data in scraped_data:

        shelf_book = ShelfBookCreate(
            title=data["title"],
            author=data["author"],
            book_url=data.get("book_url"),
            user_rating=data.get("user_rating"),
            avg_rating=data.get("avg_rating"),
            date_added = date.today()
        )

        created_book = create_shelf_book(db, shelf_book)

        created_books.append(created_book)

    return created_books