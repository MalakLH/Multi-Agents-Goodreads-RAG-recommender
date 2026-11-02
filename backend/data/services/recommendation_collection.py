import logging

from sqlalchemy.orm import Session

from backend.data.models.shelf_book import ShelfBook
from backend.data.models.recommended_book import RecommendedBook

from backend.scraper.recommendation_scraper import scrape_goodreads_carousel

logger = logging.getLogger(__name__)


async def scrape_all_recommendations(db: Session):

    # 1. Retrieve all shelf books
    shelf_books = db.query(ShelfBook).all()

    # 2. Initialize statistics
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

    # 3. Process books sequentially
    for shelf_book in shelf_books:

        print(
            f"Processing: {shelf_book.title}"
        )

        # 4. Validate source URL
        if not shelf_book.book_url:
            stats["skipped_books"] += 1

            logger.warning(
                f"Missing URL for shelf book {shelf_book.id}"
            )

            continue

        try:

            # 5. Scrape the recommendation carousel
            recommendations = await scrape_goodreads_carousel(
                shelf_book.book_url
            )

            stats["processed_books"] += 1

            stats["total_scraped"] += len(recommendations)

            # 6. Process each recommendation
            for recommendation in recommendations:

                # Validate required fields
                if not recommendation.get("title"):
                    continue

                book_url = recommendation.get("book_url")


                if not book_url:
                    continue

                # 7. Check for duplicates
                existing = db.query(RecommendedBook).filter(
                    RecommendedBook.book_url == book_url,
                    RecommendedBook.shelf_book_attached_to
                    == shelf_book.id
                ).first()

                if existing:
                    stats["duplicates"] += 1
                    continue

                # 8. Create database record
                new_recommendation = RecommendedBook(
                    title=recommendation["title"],
                    author=recommendation.get("author"),
                    rating=recommendation.get("rating"),
                    book_url=book_url,
                    shelf_book_attached_to=shelf_book.id
                )

                db.add(new_recommendation)

            # 9. Commit recommendations for this source book
            db.commit()

            logger.info(
                f"Successfully processed {shelf_book.title}"
            )

        except Exception as e:

            # 10. Roll back failed database operations
            db.rollback()

            stats["failed_books"] += 1

            stats["failures"].append({
                "shelf_book_id": shelf_book.id,
                "title": shelf_book.title,
                "error": str(e)
            })

            logger.exception(
                f"Failed to process {shelf_book.title}"
            )

            # Continue with the next shelf book
            continue

    return stats