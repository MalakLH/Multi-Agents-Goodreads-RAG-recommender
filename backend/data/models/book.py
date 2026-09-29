from pydantic import BaseModel
from typing import List, Optional

class Book(BaseModel):
    id: int
    title: str
    author: str
    avg_rating: Optional[float] = None
    genres: List[str] = []
    description: Optional[str] = None
    reviews: List[str] = []