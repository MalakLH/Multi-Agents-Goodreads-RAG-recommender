from config import openrouter_api_key

from langchain.tools import tool
from langchain.agents import create_agent


#example of a tool in langchain that can be used by the agent using the decorator @tool. 

@tool('book_recommender', description="Recommends books based on user preferences", return_direct=True)
def book_recommender_tool(user_preferences: str) -> str:
    return f"Recommended books based on your preferences: {user_preferences}"

