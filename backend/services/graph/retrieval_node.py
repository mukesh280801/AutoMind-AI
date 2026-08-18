from services.search_service import search_documents
from services.retrieval_service import get_top_k
from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger(
    "automind.graph.retrieval"
)


def retrieval_node(
    state: AutoMindState,
) -> AutoMindState:

    rewritten_question = state.get(
        "rewritten_question",
        state.get("question", ""),
    )

    intent = state.get(
        "intent",
        "search",
    )

    request_id = state.get(
        "request_id",
        "unknown",
    )

    logger.info(
        "stage=retrieval | request_id=%s | intent=%s | query=%s",
        request_id,
        intent,
        rewritten_question,
    )

    # =========================================================
    # TOP K
    # =========================================================

    top_k = get_top_k(
        intent
    )

    logger.info(
        "stage=retrieval | request_id=%s | top_k=%d",
        request_id,
        top_k,
    )

    # =========================================================
    # SEARCH
    # =========================================================

    try:

        results = search_documents(
            rewritten_question,
            limit=top_k,
        )

    except Exception as exc:

        logger.exception(
            "stage=retrieval | request_id=%s | error=%s",
            request_id,
            str(exc),
        )

        return {
            **state,
            "retrieved_chunks": [],
            "retrieval_scores": [],
            "retrieval_found": False,
            "stage": "retrieval",
        }

    # =========================================================
    # EXTRACT CHUNKS
    # =========================================================

    retrieved_chunks = []
    retrieval_scores = []

    for result in results:

        payload = result.payload or {}

        text = payload.get(
            "text",
            "",
        )

        if not text:
            continue

        score = float(
            result.score
        )

        retrieved_chunks.append(
            text
        )

        retrieval_scores.append(
            score
        )

        logger.info(
            "stage=retrieval | request_id=%s | score=%.4f",
            request_id,
            score,
        )

    retrieval_found = (
        len(retrieved_chunks) > 0
    )

    logger.info(
        "stage=retrieval | request_id=%s | chunks=%d | found=%s",
        request_id,
        len(retrieved_chunks),
        retrieval_found,
    )

    return {
        **state,

        "retrieved_chunks": (
            retrieved_chunks
        ),

        "retrieval_scores": (
            retrieval_scores
        ),

        "retrieval_found": (
            retrieval_found
        ),

        "stage": "retrieval",
    }