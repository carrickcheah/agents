import os
from langchain_openai import ChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models, QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4

# Initialize the client
client = QdrantClient(url="http://localhost:6333")

# List all collections
collections = client.get_collections()

# Print collection names
print("Available Collections:")
for collection in collections.collections:
    print(f"- {collection.name}")
