from fastapi import FastAPI

from backend.data.routers.books_router import router as book_router

app = FastAPI()

app.include_router(book_router)