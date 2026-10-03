from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from backend.qdrant.config import QDRANT_API_KEY, QDRANT_URL


# Initialize a Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define texts to embed and upload to Qdrant
texts= [
    "Apple makes very good computers.",
    "I believe Apple is innovative!",
    "I love apples.",
    "I'm a fan of Macbooks.",
    "I enjoy oranges.",
    "I like Lenovo Thinkpads.",
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

print("Texts successfully embedded and saved to Qdrant Cloud!")

print(vector_store.similarity_search("I like apples.", k=7))
print(vector_store.similarity_search("Linux is a good OS.", k=7))