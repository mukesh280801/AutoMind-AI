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

MIN_SCORE = 0.10


# ============================================================
# DOCUMENT SEARCH
# ============================================================

def search_documents(
    query: str,
    limit: int = DEFAULT_TOP_K,
):

    query = query.strip()

    if not query:
        return []

    query_embedding = model.encode(
        query
    ).tolist()

    query_lower = query.lower()


    # ========================================================
    # QUERY TYPE DETECTION
    # ========================================================

    # --------------------------------------------------------
    # Automotive-specific queries
    # --------------------------------------------------------

    is_automotive_query = (
        "bluetooth" in query_lower
        or "can bus" in query_lower
        or "can network" in query_lower
        or "controller area network" in query_lower
        or "1 mbit/s" in query_lower
        or "bit rate" in query_lower
        or "bus length" in query_lower
        or "automotive applications" in query_lower
        or "automotive document" in query_lower
        or "wireless technology" in query_lower
        or "car production" in query_lower
    )


    # --------------------------------------------------------
    # Project-list queries
    # --------------------------------------------------------

    is_list_query = (
        "what projects" in query_lower
        or "which projects" in query_lower
        or "list the projects" in query_lower
        or "projects has" in query_lower
        or "projects did" in query_lower
    )


    # --------------------------------------------------------
    # Broad knowledge queries
    # --------------------------------------------------------

    is_broad_knowledge_query = (
        "what kind of information" in query_lower
        or "what information can automind ai retrieve" in query_lower
        or "what information can automind" in query_lower
        or "what information is available" in query_lower
        or "what information is contained" in query_lower
        or "what information do the documents contain" in query_lower
        or "what topics are covered" in query_lower
    )


    # --------------------------------------------------------
    # Resume-specific queries
    # --------------------------------------------------------

    resume_keywords = [
        "resume",
        "cv",
        "dice score",
        "iou score",
        "attention u-net",
        "attention unet",
        "brain tumor",
        "lung disease",
        "f1-score",
        "f1 score",
        "adas project",
        "risk engine",
        "driving alerts",
        "developer",
        "education",
        "certification",
        "certifications",
        "professional summary",
        "technical skills",
    ]

    is_resume_query = any(
        keyword in query_lower
        for keyword in resume_keywords
    )


    # ========================================================
    # BROAD KNOWLEDGE SEARCH
    # ========================================================

    if is_broad_knowledge_query:

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=100,
            with_payload=True,
        )

        return list(
            response.points
        )


    # ========================================================
    # PROJECT LIST SEARCH
    # ========================================================

    if is_list_query:

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=100,
            with_payload=True,
        )

        resume_results = []

        for result in response.points:

            payload = result.payload or {}

            if payload.get("filename") != "Mukesh_VIT_Resume.pdf":
                continue

            if float(result.score) < MIN_SCORE:
                continue

            resume_results.append(
                result
            )

        return resume_results


    # ========================================================
    # AUTOMOTIVE DOCUMENT SEARCH
    # ========================================================

    if is_automotive_query:

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=100,
            with_payload=True,
        )

        automotive_results = []

        for result in response.points:

            payload = result.payload or {}

            if payload.get("filename") != (
                "bluetooth-in-automotive-appl.pdf"
            ):
                continue

            if float(result.score) < MIN_SCORE:
                continue

            automotive_results.append(
                result
            )

        return automotive_results[:limit]


    # ========================================================
    # RESUME DOCUMENT SEARCH
    # ========================================================

    if is_resume_query:

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=100,
            with_payload=True,
        )

        resume_results = []

        for result in response.points:

            payload = result.payload or {}

            if payload.get("filename") != (
                "Mukesh_VIT_Resume.pdf"
            ):
                continue

            if float(result.score) < MIN_SCORE:
                continue

            resume_results.append(
                result
            )

        return resume_results[:limit]


    # ========================================================
    # GENERAL SEARCH
    # ========================================================

    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit,
        with_payload=True,
    )

    results = [
        result
        for result in response.points
        if float(result.score) >= MIN_SCORE
    ]

    return results[:limit]