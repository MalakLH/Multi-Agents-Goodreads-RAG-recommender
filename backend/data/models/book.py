from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY

from backend.data.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    avg_rating = Column(String, nullable=True)
    book_url = Column(String, nullable=True)

    genres = Column(ARRAY(String), nullable=True)
    reviews = Column(ARRAY(String), nullable=True)

    description = Column(String, nullable=True)