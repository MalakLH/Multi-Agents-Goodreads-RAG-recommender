from langchain.chat_models import init_chat_model
from config import openrouter_api_key

model= init_chat_model(
    model = "qwen/qwen3.8-27b",
    model_provider= "openrouter",
    temperature= 0.2,
    max_tokens=1000,
)

message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Describe the contents of this image in detail."
        },
        {
            "type": "image_url",
            "image_url": 
            {
                "url": "https://images.unsplash.com/photo-1768595408288-22f8215ba8e9?q=80&w=1014&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            }
        }
    ]
}

response = model.invoke([message])

print(response.content)
