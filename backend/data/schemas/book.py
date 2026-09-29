from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    avg_rating: Optional[float] = None
    genres: list[str] = Field(default_factory=list)
    description: Optional[str] = None
    reviews: list[str] = Field(default_factory=list)
    book_url: Optional[str] = None


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True