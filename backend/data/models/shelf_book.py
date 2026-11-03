from sqlalchemy import Column, Integer, String, Date, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
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

    recommendations = relationship(
        "RecommendedBook",
        back_populates="source_book",
        cascade="all, delete-orphan"
    )

    recommendations_scraped = Column(
    Boolean,
    nullable=False,
    default=False,
    server_default="false"
    )

    recommendations_scraped_at = Column(
    DateTime(timezone=True),
    nullable=True
    )
    