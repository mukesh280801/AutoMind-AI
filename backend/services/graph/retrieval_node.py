from services.search_service import search_documents
from services.retrieval_service import get_top_k
from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger("automind.graph.retrieval")


def retrieval_node(state: AutoMindState) -> AutoMindState:

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

    top_k = get_top_k(intent)

    logger.info(
        "stage=retrieval | request_id=%s | top_k=%d",
        request_id,
        top_k,
    )

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
            "retrieval_sources": [],
            "retrieval_found": False,
            "stage": "retrieval",
        }

    retrieved_chunks = []
    retrieval_scores = []
    retrieval_sources = []

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

        filename = payload.get(
            "filename",
            "unknown",
        )

        chunk_id = payload.get(
            "chunk_id",
            None,
        )

        retrieved_chunks.append(
            text
        )

        retrieval_scores.append(
            score
        )

        retrieval_sources.append(
            {
                "filename": filename,
                "chunk_id": chunk_id,
                "score": score,
            }
        )

        logger.info(
            "stage=retrieval | request_id=%s | score=%.4f | filename=%s | chunk_id=%s",
            request_id,
            score,
            filename,
            chunk_id,
        )

    retrieval_found = (
        len(retrieved_chunks) > 0
    )

    logger.info(
        "stage=retrieval | request_id=%s | chunks=%d | sources=%d | found=%s",
        request_id,
        len(retrieved_chunks),
        len(retrieval_sources),
        retrieval_found,
    )

    return {
        **state,
        "retrieved_chunks": retrieved_chunks,
        "retrieval_scores": retrieval_scores,
        "retrieval_sources": retrieval_sources,
        "retrieval_found": retrieval_found,
        "stage": "retrieval",
    }