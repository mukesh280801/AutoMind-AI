from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger(
    "automind.graph.router"
)


def route_after_intent(
    state: AutoMindState,
) -> str:
    """
    Decide which path the graph should take
    based on the detected intent.
    """

    intent = state.get(
        "intent",
        ""
    )

    request_id = state.get(
        "request_id",
        "unknown",
    )

    if intent == "greeting":

        route = "response"

    elif intent == "smalltalk":

        route = "response"

    elif intent == "memory":

        route = "response"

    else:

        route = "rewrite"

    logger.info(
        "stage=router | request_id=%s | intent=%s | route=%s",
        request_id,
        intent,
        route,
    )

    return route


def route_after_retrieval(
    state: AutoMindState,
) -> str:
    """
    Decide whether relevant document chunks were found.

    If chunks exist:
        continue to compression and LLM.

    If no chunks exist:
        use the response node for the document
        fallback response.
    """

    request_id = state.get(
        "request_id",
        "unknown",
    )

    retrieved_chunks = state.get(
        "retrieved_chunks",
        [],
    )

    if retrieved_chunks:

        route = "compression"

    else:

        route = "response"

    logger.info(
        "stage=retrieval_router | request_id=%s | chunks=%d | route=%s",
        request_id,
        len(retrieved_chunks),
        route,
    )

    return route