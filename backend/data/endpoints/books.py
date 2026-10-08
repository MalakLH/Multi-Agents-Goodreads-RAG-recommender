from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.book import BookCreate, BookResponse
from crud.books import create_book
from scraper.book_scraper import scrape_book


async def scrape_and_create_book(
    url: str,
    db: Session = Depends(get_db)
) -> BookResponse:

    scraped_data = await scrape_book(url)

    book = BookCreate(
        title=scraped_data["title"],
        author=scraped_data["author"],
        description=scraped_data["description"],
        genres=scraped_data["genres"],
        reviews=scraped_data["reviews"],
        book_url=scraped_data["book_url"]
    )

    return create_book(db, book)