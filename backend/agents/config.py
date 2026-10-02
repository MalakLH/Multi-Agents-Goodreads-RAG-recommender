from dotenv import load_dotenv
import os

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

config= {
    "configurable": {
        "thread_id": 1
    }
}