from fastapi import APIRouter

from backend.data.endpoints.book_recommender import scrape_and_create_book
from backend.data.schemas.recommended_book import RecommendedBookCreate, RecommendedBookResponse


router = APIRouter(
    prefix="/recommended_books",
    tags=["RecommendedBook"]
)

router.add_api_route(
    "/scrape",
    scrape_and_create_book,
    methods=["POST"],
    response_model=list[RecommendedBookResponse]
)