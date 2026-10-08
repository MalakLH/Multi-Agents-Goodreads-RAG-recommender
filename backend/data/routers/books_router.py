from fastapi import APIRouter

from backend.data.endpoints.books import scrape_and_create_book, get_book
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
