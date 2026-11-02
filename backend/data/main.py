from fastapi import FastAPI

from backend.data.routers.books_router import router as book_router
from backend.data.routers.shelf_router import router as shelf_books_router
from backend.data.routers.recommendation_router import router as recommdendation_router

app = FastAPI()

app.include_router(book_router)
app.include_router(shelf_books_router)
app.include_router(recommdendation_router)