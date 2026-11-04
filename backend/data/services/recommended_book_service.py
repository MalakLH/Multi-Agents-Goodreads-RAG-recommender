
import asyncio
import logging

from sqlalchemy.orm import Session

from backend.data.crud.book_recommender import (
    get_recommended_book_urls
)
from backend.data.crud.books import (
    create_book,
    get_existing_book_urls
)
from backend.data.schemas.book import BookCreate
from backend.scraper.book_scraper import book_scraper


logger = logging.getLogger(__name__)


async def scrape_all_recommended_books(
    db: Session,
    delay_seconds: int = 30
):

    # 1. Get all unique recommended URLs
    recommended_urls = get_recommended_book_urls(db)

    # 2. Get URLs already stored in books
    existing_urls = get_existing_book_urls(db)

    # 3. Keep only books that haven't been scraped yet
    new_urls = [
        url for url in recommended_urls
        if url not in existing_urls
    ]

    stats = {
        "total_books": len(recommended_urls),
        "already_existing": len(recommended_urls) - len(new_urls),
        "processed": 0,
        "failed": 0,
        "failures": []
    }

    logger.info(
        f"Found {len(new_urls)} new books to scrape. "
        f"Skipping {stats['already_existing']} existing books."
    )

    # 4. Scrape only new books
    for index, url in enumerate(new_urls, start=1):

        try:
            logger.info(
                f"Processing book {index}/{len(new_urls)}: {url}"
            )

            book_data = await book_scraper(url)

            book_schema = BookCreate(**book_data)

            create_book(db, book_schema)

            stats["processed"] += 1

        except Exception as e:

            db.rollback()

            stats["failed"] += 1

            stats["failures"].append({
                "url": url,
                "error": str(e)
            })

            logger.exception(f"Failed to scrape {url}")

        # 5. Wait before the next request
        if index < len(new_urls):
            await asyncio.sleep(delay_seconds)

    return stats
