from services.graph.state import AutoMindState
from services.logging_service import get_logger

logger = get_logger("automind.graph.grounding")

NO_DOCUMENT_ANSWER = (
    "I couldn't find that information in the uploaded documents."
)


def grounding_node(state: AutoMindState) -> AutoMindState:
    """
    Check whether retrieved context appears sufficient
    before allowing the LLM to generate an answer.
    """

    question = state.get(
        "question",
        "",
    ).strip()

    context = state.get(
        "compressed_context",
        "",
    ).strip()

    request_id = state.get(
        "request_id",
        "unknown",
    )

    # ---------------------------------------------------------
    # No context
    # ---------------------------------------------------------

    if not context:

        logger.info(
            "stage=grounding | request_id=%s | supported=false | "
            "reason=no_context",
            request_id,
        )

        return {
            **state,
            "grounded": False,
            "grounding_reason": "no_context",
            "answer": NO_DOCUMENT_ANSWER,
            "stage": "grounding",
        }

    # ---------------------------------------------------------
    # Basic question/context keyword overlap
    # ---------------------------------------------------------

    question_words = {
        word.lower().strip(".,?!:;()[]{}")
        for word in question.split()
        if len(word.strip(".,?!:;()[]{}")) > 2
    }

    context_lower = context.lower()

    matched_words = [
        word
        for word in question_words
        if word in context_lower
    ]

    # ---------------------------------------------------------
    # No meaningful overlap
    # ---------------------------------------------------------

    if not matched_words:

        logger.info(
            "stage=grounding | request_id=%s | supported=false | "
            "reason=no_keyword_overlap",
            request_id,
        )

        return {
            **state,
            "grounded": False,
            "grounding_reason": "no_keyword_overlap",
            "answer": NO_DOCUMENT_ANSWER,
            "stage": "grounding",
        }

    # ---------------------------------------------------------
    # Context appears relevant
    # ---------------------------------------------------------

    logger.info(
        "stage=grounding | request_id=%s | supported=true | "
        "matched_words=%s",
        request_id,
        matched_words,
    )

    return {
        **state,
        "grounded": True,
        "grounding_reason": "context_relevant",
        "stage": "grounding",
    }