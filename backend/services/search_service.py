from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME,
    DEFAULT_TOP_K,
)

# =========================================================
# QDRANT CLIENT
# =========================================================

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)

# =========================================================
# EMBEDDING MODEL
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================================================
# SEARCH THRESHOLD
# =========================================================

# Cosine similarity.
# Queries below this threshold are treated as unrelated.
MIN_SCORE = 0.10


# =========================================================
# DOCUMENT SEARCH
# =========================================================

def search_documents(
    query: str,
    limit: int = DEFAULT_TOP_K,
):
    """
    Search Qdrant for relevant document chunks.

    Returns only chunks whose similarity score is
    above MIN_SCORE.
    """

    query = query.strip()

    if not query:
        return []

    # -----------------------------------------------------
    # Create query embedding
    # -----------------------------------------------------

    query_embedding = model.encode(
        query
    ).tolist()

    # -----------------------------------------------------
    # Query Qdrant
    # -----------------------------------------------------

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True,
    )

    results = response.points

    # -----------------------------------------------------
    # Relevance filtering
    # -----------------------------------------------------

    filtered_results = [
        result
        for result in results
        if result.score >= MIN_SCORE
    ]

    return filtered_results