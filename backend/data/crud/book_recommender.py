from backend.data.models.recommended_book import RecommendedBook
from backend.data.schemas.shelf_book import RecommendedBookCreate, RecommendedBookResponse
from sqlalchemy.orm import Session

def create_recommended_book(db: Session, recommend_book: RecommendedBookCreate) -> RecommendedBookResponse:
    db_recommend_book = RecommendedBook(**recommend_book.model_dump())

    db.add(db_recommend_book)
    db.commit()
    db.refresh(db_recommend_book)
    return db_recommend_book