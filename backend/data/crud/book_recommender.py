from backend.data.models.recommended_book import RecommendedBook
from backend.data.schemas.recommended_book import RecommendedBookCreate, RecommendedBookResponse
from sqlalchemy.orm import Session

def create_recommended_book(db: Session, recommend_book: RecommendedBookCreate) -> list[RecommendedBookResponse]:
    db_recommend_book = RecommendedBook(**recommend_book.model_dump())

    db.add(db_recommend_book)
    db.commit()
    db.refresh(db_recommend_book)
    return db_recommend_book


def get_recommended_book_urls(db: Session):
    books = (
        db.query(RecommendedBook)
        .filter(RecommendedBook.book_url.isnot(None))
        .distinct()
        .all()
    )

    return [
        book.book_url
        for book in books
    ]