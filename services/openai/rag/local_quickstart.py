import os
from langchain_openai import ChatOpenAI, AzureOpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import models, QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4



# Then we create the OpenAI and Azure OpenAI Embeddings objects
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = AzureOpenAIEmbeddings()

##########################################################################

# Initialize the client
client = QdrantClient(url="http://localhost:6333")

# Create a collection
client.create_collection(
    collection_name="test_collection",
    vectors_config=VectorParams(size=4, distance=Distance.DOT),
)

# Add vectors to the collection
operation_info = client.upsert(
    collection_name="test_collection",
    wait=True,
    points=[
        PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
        PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
        PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
        PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
        PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
        PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
    ],
)

print(operation_info)



















