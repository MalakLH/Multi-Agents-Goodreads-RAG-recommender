from pydantic import BaseModel
from typing import Optional
from datetime import date


class ShelfBookCreate(BaseModel):
    title: str
    author: str
    book_url: Optional[str] = None
    user_rating: Optional[float] = None
    avg_rating: Optional[float] = None
    date_added: Optional[date] = None


class ShelfBookResponse(ShelfBookCreate):
    id: int

    class Config:
        from_attributes = True