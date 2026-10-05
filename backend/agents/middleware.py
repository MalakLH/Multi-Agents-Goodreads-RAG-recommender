from backend.agents.config import openrouter_api_key
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, dynamic_prompt
from langchain_openrouter import ChatOpenRouter


@dataclass
class context:
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:

    user_role= request.runtime.context.user_role

    base_prompt = 'You are a helpful and very concise assistant'

    match user_role:
        case 'expert':
            return f'{base_prompt}, detail your answer as much as you can and provide technical details.'

        case 'beginner':
            return f'{base_prompt}, keep your responses as simple and basic as possible.'

        case 'child':
            return f'{base_prompt}, answer like you are talking to a literal five-year-old child.'

        case _:
            return base_prompt


model = ChatOpenRouter(
    model="qwen/qwen3.8-27b:free",
    temperature=0.2,
)


agent = create_agent(
    model=model,
    middleware= [user_role_prompt],
    context_schema=context
)

response= agent.invoke(
    {
        'messages': [{
            'role': 'user',
            'content': 'Explain TLS.'
            }]
    },
    context= context(user_role='child')
)

print(response)