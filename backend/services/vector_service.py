from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid


# ==========================================
# Qdrant Connection
# ==========================================

client = QdrantClient(
    host="localhost",
    port=16333,
)


# ==========================================
# Collection
# ==========================================

COLLECTION_NAME = "automind_docs"


# ==========================================
# Create Collection
# ==========================================

def create_collection(vector_size: int):

    collections = client.get_collections().collections

    existing = [collection.name for collection in collections]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )


# ==========================================
# Generate Stable UUID
# ==========================================

def generate_point_id(chunk: str) -> str:

    """
    Generate a deterministic UUID from the chunk text.

    The same chunk always gets the same UUID.
    """

    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            chunk
        )
    )


# ==========================================
# Store Embeddings
# ==========================================

def store_embeddings(chunks, embeddings):

    if not chunks:
        return 0

    if not embeddings:
        return 0

    create_collection(len(embeddings[0]))

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        point_id = generate_point_id(chunk)

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": chunk,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return len(points)