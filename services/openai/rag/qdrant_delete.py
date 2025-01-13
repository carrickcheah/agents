from qdrant_client import QdrantClient

# Qdrant Cloud Configuration
QDRANT_URL = "https://7201303c-5ed9-4f86-980c-b17a5d35bf26.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = "hCpTOXJL4sBv51e0ABFk8WvzJj9fJWYhQP-Esg-UeVcuJ5i8bVML5A"

# Initialize Qdrant Client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# List all collections
collections = [collection.name for collection in client.get_collections().collections]
print("Available Collections:")
for collection in collections:
    print(f"- {collection}")

# Delete all collections
for collection in collections:
    client.delete_collection(collection_name=collection)
    print(f"Deleted Collection: {collection}")

print("All collections have been deleted.")
