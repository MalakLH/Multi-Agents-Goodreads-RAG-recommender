from config import openrouter_api_key
from config import config


import requests
from dataclasses import dataclass
from typing import Optional


from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.memory import InMemorySaver


@dataclass
class BookRecommendation:
    title: str
    author: str
    release_year: Optional[int]
    reason: str


@dataclass
class SearchResult:
    books: list[BookRecommendation]


#example of a tool in langchain that can be used by the agent using the decorator @tool. 
@tool(
    "book_searcher",
    description=(
        "Searches Open Library for books based on the user's preferences. "
        "Use this tool when you need to discover books matching genres, "
        "authors, themes, styles, or other book preferences."
    ),
)
def book_searcher_tool(user_preferences: str) -> list[dict]:

    print("\n=== BOOK SEARCHER ===")
    print("Query:", user_preferences)

    response = requests.get(
        "https://openlibrary.org/search.json",
        params={
            "q": user_preferences,
            "limit": 10,
            "fields": "title,author_name,first_publish_year,key,cover_i",
        },
        headers={
            "User-Agent": "GoodreadsRAGRecommender/1.0"
        },
        timeout=10,
    )

    print("Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    print("Number of results:", len(data.get("docs", [])))
    print("First result:", data.get("docs", [])[:1])

    books = []

    for book in data.get("docs", []):
        authors = book.get("author_name", [])

        books.append({
            "title": book.get("title"),
            "author": authors[0] if authors else "Unknown",
            "release_year": book.get("first_publish_year"),
            "open_library_key": book.get("key"),
            "cover_id": book.get("cover_i"),
        })

    print("Books returned:", books)

    return books

#need to specify that you're using openrouter as the model provider
model = ChatOpenRouter(
    model="qwen/qwen3.8-27b:free",
    temperature=0.2,
)

checkpointer= InMemorySaver()

agent = create_agent(

    model=model,
    tools=[book_searcher_tool],
    response_format=SearchResult,
    checkpointer=checkpointer,
    system_prompt=(
        """
You are a book recommendation agent.

Use the book_searcher tool to find books.

Only recommend books that were returned by the tool.

Return your final answer using the required ResponseFormat structure.

For each recommendation, provide:
- title
- author
- release_year
- a short reason explaining why it matches the user's preferences.
"""
    ),
)

try:

    response = agent.invoke({

        "messages": [
            {
                "role": "user",
                "content": "I like classics like Crime and Punishment, but I also enjoy modern thrillers. Can you recommend some books for me?"
            }
        ]
    },
        config=config,
)

    print(response)
    print(response["messages"][-1].content)

except Exception as e:
    print(f"An agent error occurred: {e}")


try:

    response = agent.invoke({

        "messages": [
            {
                "role": "user",
                "content": "what's the best among them?"
            }
        ]
    },
        config=config,
)

    print(response)
    print(response["messages"][-1].content)

except Exception as e:
    print(f"An agent error occurred: {e}")