from pydantic import BaseModel, HttpUrl
from typing import Optional

class RecommendedBook(BaseModel):
    id: int
    title: str
    author: str
    rating: Optional[float] = None
    book_url: Optional[HttpUrl] = None
    shelf_book_attached_to: Optional[int] = None