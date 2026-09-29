from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.data.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    avg_rating: Mapped[float | None] = mapped_column(Float)
    description: Mapped[str | None] = mapped_column(String)