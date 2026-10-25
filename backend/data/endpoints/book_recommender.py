from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.data.db.database import get_db
from backend.data.schemas.book import BookCreate, BookResponse
from backend.data.crud.books import create_recommended_book
from backend.scraper.book_scraper import book_scraper


async def scrape_and_create_book(
    url: str,
    db: Session = Depends(get_db)
) -> BookResponse:

    scraped_data = await book_scraper(url)

    book = BookCreate(
        title=scraped_data["title"],
        author=scraped_data["author"],
        rating=scraped_data["rating"],
        book_url=scraped_data["book_url"]
    )

    return create_recommended_book(db, book)

    shelf_book_attached_to: Optional[int] = None
