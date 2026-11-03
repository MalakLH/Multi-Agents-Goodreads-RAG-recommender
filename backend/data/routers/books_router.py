from fastapi import APIRouter

from backend.data.endpoints.books import scrape_and_create_book, get_book, scrape_recommended_details
from backend.data.schemas.book import BookResponse


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

router.add_api_route(
    "/scrape",
    scrape_and_create_book,
    methods=["POST"],
    response_model=BookResponse
)

router.add_api_route(
    "/{title}",
    get_book,
    methods=["GET"],
    response_model=BookResponse
)

router.add_api_route(
    "/urls",
    scrape_recommended_details,
    methods=["POST"],
    response_model=list[str]
)