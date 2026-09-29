from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date


class ShelfBook(BaseModel):
    id: int
    title: str
    author: str
    book_url: Optional[HttpUrl] = None
    user_rating: Optional[float] = None
    avg_rating: Optional[float] = None
    date_added: Optional[date] = None