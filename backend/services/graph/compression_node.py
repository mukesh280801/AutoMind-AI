from services.compression_service import compress_context
from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger(
    "automind.graph.compression"
)


def compression_node(
    state: AutoMindState,
) -> AutoMindState:

    question = state.get(
        "rewritten_question",
        state.get("question", ""),
    )

    chunks = state.get(
        "retrieved_chunks",
        [],
    )

    request_id = state.get(
        "request_id",
        "unknown",
    )

    logger.info(
        "stage=compression | request_id=%s | chunks=%d",
        request_id,
        len(chunks),
    )

    # =========================================================
    # NO RETRIEVAL
    # =========================================================

    if not chunks:

        return {
            **state,
            "compressed_context": "",
            "stage": "compression",
        }

    # =========================================================
    # COMPRESS
    # =========================================================

    try:

        compressed_context = compress_context(
            question,
            chunks,
        )

    except Exception as exc:

        logger.exception(
            "stage=compression | request_id=%s | error=%s",
            request_id,
            str(exc),
        )

        compressed_context = (
            "\n\n".join(chunks)
        )

    logger.info(
        "stage=compression | request_id=%s | chars=%d",
        request_id,
        len(compressed_context),
    )

    return {
        **state,
        "compressed_context": (
            compressed_context
        ),
        "stage": "compression",
    }