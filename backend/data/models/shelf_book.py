from sqlalchemy import Column, Integer, String, Float, Date
from backend.data.db.database import Base


class ShelfBook(Base):
    __tablename__ = "shelf_books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    book_url = Column(String, nullable=True)
    user_rating = Column(Float, nullable=True)
    avg_rating = Column(Float, nullable=True)
    date_added = Column(Date, nullable=True)