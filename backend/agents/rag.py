from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant

# Initialize a Hugging Face embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Embed a single query
query_vector = embeddings.embed_query("Explain LangChain embeddings")

# Embed multiple documents
doc_vectors = embeddings.embed_documents(["Document 1 text", "Document 2 text"])
