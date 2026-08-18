from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger("automind.graph.memory")


def memory_node(state: AutoMindState) -> AutoMindState:
    """
    Load conversation history from the current
    LangGraph thread checkpoint.

    LangGraph restores the previous state automatically
    when the same thread_id is used.
    """

    request_id = state.get(
        "request_id",
        "unknown"
    )

    history = state.get(
        "history",
        []
    )

    logger.info(
        "stage=memory | request_id=%s | history_messages=%d",
        request_id,
        len(history),
    )

    return {
        **state,
        "history": history,
        "stage": "memory",
    }