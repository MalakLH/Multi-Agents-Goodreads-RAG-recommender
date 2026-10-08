from pydantic import BaseModel
from typing import Optional


class RecommendedBookCreate(BaseModel):
    title: str
    author: str
    rating: Optional[str] = None
    book_url: Optional[str] = None
    shelf_book_attached_to: Optional[int] = None


class RecommendedBookResponse(RecommendedBookCreate):
    id: int

    class Config:
        from_attributes = True