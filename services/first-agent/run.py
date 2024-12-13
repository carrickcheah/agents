import openai
import qdrant_client

print("Initializing OpenAI and Qdrant clients...")

openai_client = openai.Client()
client = qdrant_client.QdrantClient(":memory:")

texts = [
    "Qdrant is the best vector search engine!",
    "Loved by Enterprises and everyone building for low latency, high performance, and scale.",
]

print("Texts to be embedded:", texts)

embedding_model = "text-embedding-3-small"

print("Generating embeddings for texts...")
result = openai_client.embeddings.create(input=texts, model=embedding_model)

print("Embeddings generated successfully!")
print("Embedding result:", result)

from qdrant_client.models import PointStruct

points = [
    PointStruct(
        id=idx,
        vector=data.embedding,
        payload={"text": text},
    )
    for idx, (data, text) in enumerate(zip(result.data, texts))
]

print("Points created for Qdrant:", points)

from qdrant_client.models import VectorParams, Distance

collection_name = "example_collection"

print(f"Creating collection '{collection_name}' in Qdrant...")
client.create_collection(
    collection_name,
    vectors_config=VectorParams(
        size=1536,
        distance=Distance.COSINE,
    ),
)
print(f"Collection '{collection_name}' created successfully!")

print("Upserting points into the collection...")
client.upsert(collection_name, points)
print("Points inserted into Qdrant successfully!")

print("Performing a search query...")
query_embedding = openai_client.embeddings.create(
    input=["What is the best to use for vector search scaling?"],
    model=embedding_model,
).data[0].embedding

search_results = client.search(
    collection_name=collection_name,
    query_vector=query_embedding,
)

print("Search completed successfully!")
print("Search results:", search_results)
