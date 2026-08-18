from services.intent_service import detect_intent
from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger("automind.graph.intent")


def intent_node(state: AutoMindState) -> AutoMindState:
    """
    Detect the intent of the user's question
    and store it in the graph state.
    """

    question = state["question"]

    logger.info(
        "stage=intent | request_id=%s | question=%s",
        state.get("request_id", "unknown"),
        question
    )

    intent = detect_intent(question)

    logger.info(
        "stage=intent | request_id=%s | detected_intent=%s",
        state.get("request_id", "unknown"),
        intent
    )

    return {
        **state,
        "intent": intent,
        "stage": "intent",
    }