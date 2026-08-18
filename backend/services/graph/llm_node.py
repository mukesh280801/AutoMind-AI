from services.graph.state import AutoMindState
from services.logging_service import get_logger
from services.llm_service import generate_answer


logger = get_logger(
    "automind.graph.llm"
)


NO_DOCUMENT_ANSWER = (
    "I couldn't find that information in the uploaded documents."
)


LLM_ERROR_ANSWER = (
    "I couldn't generate an answer from the uploaded documents."
)


def llm_node(
    state: AutoMindState,
) -> AutoMindState:

    question = state.get(
        "question",
        "",
    )

    context = state.get(
        "compressed_context",
        "",
    )

    retrieved_chunks = state.get(
        "retrieved_chunks",
        [],
    )

    history = state.get(
        "history",
        [],
    )

    request_id = state.get(
        "request_id",
        "unknown",
    )

    # =========================================================
    # GROUNDING CHECK
    # =========================================================

    if not retrieved_chunks:

        logger.info(
            "stage=llm | request_id=%s | grounded=false | "
            "reason=no_retrieval",
            request_id,
        )

        return {
            **state,
            "answer": NO_DOCUMENT_ANSWER,
            "stage": "llm",
        }

    if not context.strip():

        logger.info(
            "stage=llm | request_id=%s | grounded=false | "
            "reason=no_context",
            request_id,
        )

        return {
            **state,
            "answer": NO_DOCUMENT_ANSWER,
            "stage": "llm",
        }

    # =========================================================
    # LOGGING
    # =========================================================

    logger.info(
        "stage=llm | request_id=%s | grounded=true | "
        "chunks=%d | context_chars=%d",
        request_id,
        len(retrieved_chunks),
        len(context),
    )

    # =========================================================
    # GENERATE
    # =========================================================

    try:

        answer = generate_answer(
            question=question,
            context=context,
            history=history,
        )

    except Exception as exc:

        logger.exception(
            "stage=llm | request_id=%s | error=%s",
            request_id,
            str(exc),
        )

        return {
            **state,
            "answer": LLM_ERROR_ANSWER,
            "stage": "llm",
        }

    # =========================================================
    # EMPTY RESPONSE
    # =========================================================

    if not answer:

        answer = NO_DOCUMENT_ANSWER

    answer = str(
        answer
    ).strip()

    logger.info(
        "stage=llm | request_id=%s | answer_chars=%d",
        request_id,
        len(answer),
    )

    return {
        **state,
        "answer": answer,
        "stage": "llm",
    }