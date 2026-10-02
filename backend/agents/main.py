from config import openrouter_api_key

from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

#example of a tool in langchain that can be used by the agent using the decorator @tool. 

@tool('book_recommender', description="Recommends books based on user preferences", return_direct=True)
def book_recommender_tool(user_preferences: str) -> str:
    return f"Recommended books based on your preferences: {user_preferences}"



#need to specify that you're using openrouter as the model provider
model = ChatOpenRouter(
    model="openrouter/free",
    temperature=0,
)


agent = create_agent(

    model=model,
    tools=[book_recommender_tool],
    system_prompt="You are a humorous book recommender agent who always likes to make jokes and puns about books. You are also very knowledgeable about books and can provide recommendations based on user preferences.",

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