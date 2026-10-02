from config import openrouter_api_key


import requests
from dataclasses import dataclass


from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter



@dataclass
class BookRecommendation:
    title: str
    author: str
    release_year: int


@dataclass
class SearchResult:
    books: list[BookRecommendation]


#example of a tool in langchain that can be used by the agent using the decorator @tool. 

@tool('book_searcher', description="searches books based on user preferences", return_direct=True)
def book_searcher_tool(user_preferences: str) -> list:
    """
    Searches for books based on user preferences.
    Args:
        user_preferences (str): User preferences for book search.
    """




#need to specify that you're using openrouter as the model provider
model = ChatOpenRouter(
    model="openrouter/free",
    temperature=0.2,
)


agent = create_agent(

    model=model,
    tools=[book_searcher_tool],
    system_prompt="You are a humorous book searcher agent who always likes to make jokes and puns about books. You are also very knowledgeable about books and can provide search results based on user preferences.",
    response_format=SearchResult

)
try:

    response = agent.invoke({

        "messages": [
            {
                "role": "user",
                "content": "I like classics like Crime and Punishment, but I also enjoy modern thrillers. Can you recommend some books for me?"
            }
        ]
    }
)

    print(response)
    print(response["messages"][-1].content)

except Exception as e:
    print(f"An agent error occurred: {e}")