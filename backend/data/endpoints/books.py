from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.data.db.database import get_db
from backend.data.schemas.book import BookCreate, BookResponse
from backend.data.crud.books import create_book, get_book_by_title
from backend.scraper.book_scraper import book_scraper


async def scrape_and_create_book(
    url: str,
    db: Session = Depends(get_db)
) -> BookResponse:

    scraped_data = await book_scraper(url)

    book = BookCreate(
        title=scraped_data["title"],
        author=scraped_data["author"],
        description=scraped_data["description"],
        genres=scraped_data["genres"],
        reviews=scraped_data["reviews"],
        book_url=scraped_data["book_url"]
    )

    return create_book(db, book)


def get_book(title: str, db: Session = Depends(get_db)):
    book = get_book_by_title(db, title)

    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book '{title}' not found"
        )

    return book