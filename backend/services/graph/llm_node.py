from services.graph.state import AutoMindState
from services.logging_service import get_logger
from services.llm_service import generate_answer


logger = get_logger("automind.graph.llm")


NO_DOCUMENT_ANSWER = (
    "I couldn't find that information in the uploaded documents."
)

LLM_ERROR_ANSWER = (
    "I couldn't generate an answer from the uploaded documents."
)


def _context_has_information(context: str) -> bool:
    if not context:
        return False

    cleaned = context.strip()

    if not cleaned:
        return False

    return True


def llm_node(
    state: AutoMindState,
) -> AutoMindState:

    question = state.get(
        "question",
        "",
    )

    compressed_context = state.get(
        "compressed_context",
        "",
    )

    retrieved_chunks = state.get(
        "retrieved_chunks",
        [],
    )

    request_id = state.get(
        "request_id",
        "unknown",
    )

    history = state.get(
        "history",
        [],
    )

    if history is None:
        history = []

    # =====================================================
    # No retrieved documents
    # =====================================================

    if not retrieved_chunks:

        logger.info(
            "stage=llm | request_id=%s | "
            "grounded=false | reason=no_chunks",
            request_id,
        )

        answer = NO_DOCUMENT_ANSWER

        updated_history = history + [
            {
                "role": "user",
                "content": question,
            },
            {
                "role": "assistant",
                "content": answer,
            },
        ]

        return {
            **state,
            "answer": answer,
            "history": updated_history,
            "stage": "llm",
        }

    # =====================================================
    # No usable context
    # =====================================================

    if not _context_has_information(
        compressed_context
    ):

        logger.info(
            "stage=llm | request_id=%s | "
            "grounded=false | reason=no_context",
            request_id,
        )

        answer = NO_DOCUMENT_ANSWER

        updated_history = history + [
            {
                "role": "user",
                "content": question,
            },
            {
                "role": "assistant",
                "content": answer,
            },
        ]

        return {
            **state,
            "answer": answer,
            "history": updated_history,
            "stage": "llm",
        }

    # =====================================================
    # Generate grounded answer
    # =====================================================

    logger.info(
        "stage=llm | request_id=%s | "
        "grounded=true | chunks=%d | context_chars=%d",
        request_id,
        len(retrieved_chunks),
        len(compressed_context),
    )

    try:

        answer = generate_answer(
            question=question,
            context=compressed_context,
            history=history,
        )

    except Exception as exc:

        logger.exception(
            "stage=llm | request_id=%s | "
            "error=%s",
            request_id,
            exc,
        )

        answer = LLM_ERROR_ANSWER

    # =====================================================
    # Normalize answer
    # =====================================================

    if not answer:

        answer = NO_DOCUMENT_ANSWER

    answer = str(answer).strip()

    if not answer:

        answer = NO_DOCUMENT_ANSWER

    # =====================================================
    # UPDATE CONVERSATION HISTORY
    # =====================================================

    updated_history = history + [
        {
            "role": "user",
            "content": question,
        },
        {
            "role": "assistant",
            "content": answer,
        },
    ]

    # =====================================================
    # Logging
    # =====================================================

    logger.info(
        "stage=llm | request_id=%s | "
        "answer_chars=%d",
        request_id,
        len(answer),
    )

    logger.info(
        "stage=llm | request_id=%s | "
        "history_messages=%d",
        request_id,
        len(updated_history),
    )

    # =====================================================
    # Return updated state
    # =====================================================

    return {
        **state,
        "answer": answer,
        "history": updated_history,
        "stage": "llm",
    }