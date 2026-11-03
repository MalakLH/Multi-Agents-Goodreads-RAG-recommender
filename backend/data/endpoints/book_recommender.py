
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.data.db.database import get_db
from backend.data.models.shelf_book import ShelfBook
from backend.data.schemas.recommended_book import (
    RecommendedBookCreate,
    RecommendedBookResponse
)
from backend.data.crud.book_recommender import create_recommended_book
from backend.scraper.recommendation_scraper import scrape_goodreads_carousel
from backend.data.services.recommendation_collection import scrape_all_recommendations


async def scrape_and_create_book(
    url: str,
    db: Session = Depends(get_db)
):

    # 1. Find the original book in the user's shelf
    shelf_book = db.query(ShelfBook).filter(
        ShelfBook.book_url == url
    ).first()

    if not shelf_book:
        raise HTTPException(
            status_code=404,
            detail="Book not found in the user's shelf."
        )

    # 2. Scrape Goodreads recommendations
    scraped_books = await scrape_goodreads_carousel(url)

    # 3. Save each recommendation
    created_books = []

    for scraped_book in scraped_books:

        book = RecommendedBookCreate(
            title=scraped_book["title"],
            author=scraped_book["author"],
            rating=scraped_book["rating"],
            book_url=scraped_book["book_url"],
            shelf_book_attached_to=shelf_book.id
        )

        created_book = create_recommended_book(db, book)
        created_books.append(created_book)

    return created_books

async def scrape_all(db: Session = Depends(get_db)):

    result = await scrape_all_recommendations(db)

    return result

