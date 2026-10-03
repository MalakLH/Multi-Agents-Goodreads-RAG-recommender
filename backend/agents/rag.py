from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter

from backend.qdrant.config import QDRANT_API_KEY, QDRANT_URL
from backend.agents.config import openrouter_api_key

# Initialize a Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define texts to embed and upload to Qdrant
texts= [
    "I hate bananas.",
    "I despise mangos.",
    "I love apples.",
    "I dislike windows.",
    "I enjoy oranges.",
    "I like Linux.",
    "I think pears taste very good."
]

# Generate embeddings and upload to Qdrant Cloud
vector_store = QdrantVectorStore.from_texts(
    texts=texts,
    embedding=embeddings,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name="my_cloud_test",
)

#print("Texts successfully embedded and saved to Qdrant Cloud!")

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# we pass the retriever to create a tool that can be used by the agent.
retriever_tool = create_retriever_tool(
    retriever=retriever,
    name="fruit_retriever",
    description="Retrieves information about the user's fruit preferences from the vector store.",
)

model = ChatOpenRouter(
    model = "openrouter/free",
    max_retries=3,
    temperature=0.2
)

# now we create the agent and we pass the new retrieval tool to it.
agent = create_agent(
    model = model,
    tools= [retriever_tool],
    system_prompt= (
        "You are a helpful assistant. for questions related to fruits"
        "call the retriever tool to get context then answer."
        "Maybe you have to use it multiple times before answering."
    ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What are the three fruits does the person like and what are the three fruits does this person dislike?"
            }
        ]
    }
)

print(result)
print(result["messages"][-1].content)