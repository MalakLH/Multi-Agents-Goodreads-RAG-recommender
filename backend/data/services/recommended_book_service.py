import asyncio
import logging

from sqlalchemy.orm import Session

from backend.data.crud.book_recommender import (
    get_recommended_book_urls
)
from backend.data.crud.books import create_book
from backend.data.schemas.book import BookCreate
from backend.scraper.book_scraper import book_scraper


logger = logging.getLogger(__name__)


async def scrape_all_recommended_books(
    db: Session,
    delay_seconds: int = 30
):
    urls = get_recommended_book_urls(db)

    stats = {
        "total_books": len(urls),
        "processed": 0,
        "failed": 0,
        "failures": []
    }

    for index, url in enumerate(urls, start=1):

        try:
            logger.info(
                f"Processing book {index}/{len(urls)}: {url}"
            )

            book_data = await book_scraper(url)

            book_schema = BookCreate(**book_data)

            create_book(db, book_schema)

            stats["processed"] += 1

        except Exception as e:
            stats["failed"] += 1

            stats["failures"].append({
                "url": url,
                "error": str(e)
            })

            logger.exception(f"Failed to scrape {url}")

        # Wait before the next request
        if index < len(urls):
            await asyncio.sleep(delay_seconds)

    return stats