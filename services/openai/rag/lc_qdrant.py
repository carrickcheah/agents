import os
from langchain_openai import ChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4



# Then we create the OpenAI and Azure OpenAI Embeddings objects
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = AzureOpenAIEmbeddings()

##########################################################################


# Qdrant Cloud Configuration
QDRANT_URL = "https://7201303c-5ed9-4f86-980c-b17a5d35bf26.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "hCpTOXJL4sBv51e0ABFk8WvzJj9fJWYhQP-Esg-UeVcuJ5i8bVML5A"

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Check existing collections
print(f"Existing Collections: {client.get_collections()}")

# Create or recreate the collection with the correct dimensions
COLLECTION_NAME = "demo_collection"
VECTOR_SIZE = 3072  # Match the embedding size

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
)

# Initialize Qdrant Vector Store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=None,  # Replace with your actual embedding model
    force_recreate=True,  # Recreate collection if dimensions mismatch
)

# Add documents
documents = [
    Document(page_content="I had chocolate chip pancakes for breakfast.", metadata={"source": "tweet"}),
    Document(page_content="The weather forecast is cloudy and overcast.", metadata={"source": "news"}),
    Document(page_content="Building an exciting new project with LangChain!", metadata={"source": "tweet"}),
]

uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)
print("Documents successfully added to Qdrant Cloud!")

# Query the vector store
QUERY_TEXT = "What's the weather forecast?"
query_results = vector_store.similarity_search(query=QUERY_TEXT, k=2)

# Display query results
for result in query_results:
    print(f"* {result.page_content} [{result.metadata}]")
