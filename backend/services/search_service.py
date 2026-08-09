from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME,
    DEFAULT_TOP_K
)

# ==========================
# Connect to Qdrant
# ==========================

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)

# ==========================
# Load Embedding Model
# ==========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def search_documents(
    query: str,
    limit: int = DEFAULT_TOP_K
):
    """
    Search the Qdrant vector database for
    the most relevant document chunks.
    """

    # Convert question to embedding
    query_embedding = model.encode(query).tolist()

    # Search Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
    )

    return results.points