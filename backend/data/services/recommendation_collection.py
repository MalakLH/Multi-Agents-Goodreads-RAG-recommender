
import logging

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.data.models.shelf_book import ShelfBook
from backend.data.models.recommended_book import RecommendedBook
from backend.scraper.recommendation_scraper import (
    scrape_goodreads_carousel
)

logger = logging.getLogger(__name__)


async def scrape_all_recommendations(db: Session):

    # 1. Retrieve shelf books that haven't been scraped successfully
    shelf_books = (
        db.query(ShelfBook)
        .filter(ShelfBook.recommendations_scraped.is_(False))
        .all()
    )

    # 2. Initialize scraping statistics
    stats = {
        "total_books": len(shelf_books),
        "processed_books": 0,
        "failed_books": 0,
        "skipped_books": 0,
        "total_scraped": 0,
        "inserted": 0,
        "duplicates": 0,
        "failures": []
    }

    # 3. Process shelf books sequentially
    for shelf_book in shelf_books:

        logger.info(
            f"Processing shelf book {shelf_book.id}: "
            f"{shelf_book.title}"
        )

        # 4. Skip books without a Goodreads URL
        if not shelf_book.book_url:
            stats["skipped_books"] += 1

            logger.warning(
                f"Missing URL for shelf book {shelf_book.id}"
            )
            continue

        try:
            # 5. Scrape the Goodreads recommendation carousel
            recommendations = await scrape_goodreads_carousel(
                shelf_book.book_url
            )

            stats["total_scraped"] += len(recommendations)

            inserted_count = 0
            duplicate_count = 0

            # Prevent duplicate URLs within the same carousel
            seen_urls = set()

            # 6. Process each scraped recommendation
            for recommendation in recommendations:

                title = recommendation.get("title")
                book_url = recommendation.get("book_url")

                # Ignore incomplete records
                if not title or not book_url:
                    continue

                # Ignore duplicate URLs in the current carousel
                if book_url in seen_urls:
                    duplicate_count += 1
                    continue

                seen_urls.add(book_url)

                # 7. Check whether this recommendation already exists
                existing = (
                    db.query(RecommendedBook)
                    .filter(
                        RecommendedBook.book_url == book_url,
                        RecommendedBook.shelf_book_attached_to
                        == shelf_book.id
                    )
                    .first()
                )

                if existing:
                    duplicate_count += 1
                    continue

                # 8. Create the recommendation record
                new_recommendation = RecommendedBook(
                    title=title.strip(),
                    author=(
                        recommendation.get("author") or "Unknown"
                    ).strip(),
                    rating=recommendation.get("rating"),
                    book_url=book_url,
                    shelf_book_attached_to=shelf_book.id
                )

                db.add(new_recommendation)
                inserted_count += 1

            # 9. Mark this shelf book as successfully scraped
            shelf_book.recommendations_scraped = True
            shelf_book.recommendations_scraped_at = datetime.now(
                timezone.utc
            )

            # 10. Commit recommendations and scraping status together
            db.commit()

            # 11. Update statistics after successful commit
            stats["processed_books"] += 1
            stats["inserted"] += inserted_count
            stats["duplicates"] += duplicate_count

            logger.info(
                f"Successfully processed '{shelf_book.title}': "
                f"{inserted_count} inserted, "
                f"{duplicate_count} duplicates"
            )

        except Exception as e:

            # Roll back all changes for this shelf book
            db.rollback()

            stats["failed_books"] += 1

            stats["failures"].append({
                "shelf_book_id": shelf_book.id,
                "title": shelf_book.title,
                "error": str(e)
            })

            logger.exception(
                f"Failed to process '{shelf_book.title}'"
            )

            continue

    logger.info(
        "Scraping completed: "
        f"{stats['processed_books']} processed, "
        f"{stats['failed_books']} failed, "
        f"{stats['inserted']} inserted"
    )

    return stats
