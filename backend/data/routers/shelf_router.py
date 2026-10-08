from fastapi import APIRouter

from backend.data.endpoints.shelf_books import scrape_and_create_shelf_book
from backend.data.schemas.shelf_book import ShelfBookResponse


router = APIRouter(
    prefix="/shelf_books",
    tags=["ShelfBooks"]
)

router.add_api_route(
    "/shelf_books",
    scrape_and_create_shelf_book,
    methods=["POST"],
    response_model=list[ShelfBookResponse]
)