import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing_extensions import List, TypedDict
from qdrant_client.models import VectorParams, Distance

# First we export related environment variables into terminal:
# 1. OpenAI API key 
# 2. Azure API key as environment variables
# 3. Langchain api key

# export OPENAI_API_KEY=your_openai_key
# export AZURE_OPENAI_ENDPOINT=your_endpoint
# export AZURE_OPENAI_DEPLOYMENT_NAME=text-embedding-3-large
# export AZURE_OPENAI_API_VERSION=1
# export LANGCHAIN_TRACING_V2="true"
# export LANGCHAIN_API_KEY=your_langchain_api_key


# Then we create the OpenAI and Azure OpenAI Embeddings objects
llm = ChatOpenAI(model="gpt-4o-mini")
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


# Option 1: In-Memory Vector Store
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# # Option 2: Qdrant Vector Store
# client = QdrantClient(path="./services/openai")
# client.create_collection(
#     collection_name="demo_collection",
#     vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
# )

# vector_store = QdrantVectorStore(
#     client=client,
#     collection_name="demo_collection",
#     embedding=embeddings,
# )

# # chroma, faiss, pinecone,pgvector
# from langchain_chroma import Chroma
# vector_store = Chroma(embedding_function=embeddings)
url = url="http://localhost:6333"
docs = []  # put docs here
qdrant = QdrantVectorStore.from_documents(
    docs,
    embeddings,
    url=url,
    prefer_grpc=True,
    collection_name="my_documents",
)

import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

# Load and chunk contents of the blog
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index chunks
_ = vector_store.add_documents(documents=all_splits)

# Define prompt for question-answering
prompt = hub.pull("rlm/rag-prompt")


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


response = graph.invoke({"question": "What is Task Decomposition?"})
print(response["answer"])







