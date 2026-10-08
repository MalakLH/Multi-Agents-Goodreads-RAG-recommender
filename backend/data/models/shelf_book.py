from sqlalchemy import Column, Integer, String, Date
from backend.data.db.database import Base


class ShelfBook(Base):
    __tablename__ = "shelf_books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    book_url = Column(String, nullable=True)
    user_rating = Column(String, nullable=True)
    avg_rating = Column(String, nullable=True)
    date_added = Column(Date, nullable=True)