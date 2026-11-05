import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

if not openrouter_api_key:
    raise ValueError("OPENROUTER_API_KEY is missing")

llm = ChatOpenAI(
    model="openrouter/free",
    openai_api_key=openrouter_api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0
)