from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from config import (
    QDRANT_HOST,
    QDRANT_PORT,
    COLLECTION_NAME,
    DEFAULT_TOP_K,
)


# ============================================================
# QDRANT + EMBEDDING MODEL
# ============================================================

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT,
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Minimum semantic similarity score
MIN_SCORE = 0.10


# ============================================================
# DOCUMENT SEARCH
# ============================================================

def search_documents(
    query: str,
    limit: int = DEFAULT_TOP_K,
):
    """
    Search uploaded documents from Qdrant.

    Automotive queries:
        - Search broadly across automotive documents.
        - Resume is excluded.

    List/project queries:
        - Retrieve more chunks for better coverage.

    Normal queries:
        - Use semantic similarity filtering.
    """

    query = query.strip()

    if not query:
        return []

    # --------------------------------------------------------
    # Create query embedding
    # --------------------------------------------------------

    query_embedding = model.encode(
        query
    ).tolist()

    query_lower = query.lower()

    # ========================================================
    # QUERY TYPE DETECTION
    # ========================================================

    # Broad list / project questions need more chunks
    is_list_query = (
        "what projects" in query_lower
        or "which projects" in query_lower
        or "list the projects" in query_lower
        or "projects has" in query_lower
        or "projects did" in query_lower
    )

    # Automotive-related questions
    #
    # Important:
    # Do NOT hardcode one specific automotive PDF.
    # Any uploaded automotive document should be searchable.
    #
    is_automotive_query = (
        "automotive" in query_lower
        or "bluetooth" in query_lower
        or "can" in query_lower
        or "can bus" in query_lower
        or "can network" in query_lower
        or "controller area network" in query_lower
        or "bit rate" in query_lower
        or "mbit/s" in query_lower
        or "kbit/s" in query_lower
        or "bus length" in query_lower
        or "vehicle" in query_lower
        or "ecu" in query_lower
        or "diagnostic" in query_lower
        or "diagnostics" in query_lower
        or "adas" in query_lower
        or "radar" in query_lower
        or "camera" in query_lower
        or "powertrain" in query_lower
        or "brake" in query_lower
        or "engine" in query_lower
        or "automotive applications" in query_lower
        or "automotive document" in query_lower
        or "wireless technology" in query_lower
        or "car production" in query_lower
    )

    # ========================================================
    # RETRIEVAL LIMIT
    # ========================================================

    if is_list_query:
        retrieval_limit = 100

    elif is_automotive_query:
        # Search wider so relevant automotive chunks
        # from multiple automotive PDFs can be found.
        retrieval_limit = max(100, limit)

    else:
        retrieval_limit = limit

    # ========================================================
    # QDRANT SEARCH
    # ========================================================

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=retrieval_limit,
        with_payload=True,
    )

    print(
        "RAW QDRANT COUNT:",
        len(response.points),
    )

    # ========================================================
    # AUTOMOTIVE SEARCH
    # ========================================================

    if is_automotive_query:

        automotive_results = []

        for result in response.points:

            payload = result.payload or {}

            filename = payload.get(
                "filename",
                "",
            )

            score = float(
                result.score
            )

            print(
                "AUTOMOTIVE SCORE:",
                filename,
                round(score, 4),
            )

            # ------------------------------------------------
            # Exclude resume from automotive retrieval
            # ------------------------------------------------

            if filename == "Mukesh_VIT_Resume.pdf":
                continue

            # ------------------------------------------------
            # Apply minimum similarity score
            # ------------------------------------------------

            if score < MIN_SCORE:
                continue

            automotive_results.append(
                result
            )

        return automotive_results[:limit]

    # ========================================================
    # LIST / PROJECT QUERY
    # ========================================================

    if is_list_query:

        # List queries need wider coverage.
        # Keep all retrieved chunks.
        results = list(
            response.points
        )

        return results[:retrieval_limit]

    # ========================================================
    # NORMAL SEMANTIC SEARCH
    # ========================================================

    results = [
        result
        for result in response.points
        if float(result.score) >= MIN_SCORE
    ]

    return results[:limit]