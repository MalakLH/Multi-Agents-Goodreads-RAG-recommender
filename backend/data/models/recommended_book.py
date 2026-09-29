from sqlalchemy import Column, Integer, String, Float, ForeignKey
from backend.data.db.database import Base


class RecommendedBook(Base):
    __tablename__ = "recommended_books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    book_url = Column(String, nullable=True)

    shelf_book_attached_to = Column(
        Integer,
        ForeignKey("shelf_books.id"),
        nullable=True
    )