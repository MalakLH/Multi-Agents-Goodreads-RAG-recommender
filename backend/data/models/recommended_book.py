from sqlalchemy import Column, Integer, String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.data.db.database import Base


class RecommendedBook(Base):
    __tablename__ = "recommended_books"

    __table_args__ = (
        UniqueConstraint(
            "book_url",
            "shelf_book_attached_to",
            name="unique_book_per_source"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    author = Column(String)

    rating = Column(Float)
    book_url = Column(String, nullable=False)

    shelf_book_attached_to = Column(
        Integer,
        ForeignKey("shelf_books.id", ondelete="CASCADE"),
        nullable=False
    )

    source_book = relationship(
        "ShelfBook",
        back_populates="recommendations"
    )