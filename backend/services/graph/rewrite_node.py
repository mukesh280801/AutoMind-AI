from services.query_rewrite_service import rewrite_question
from services.graph.state import AutoMindState


def rewrite_node(state: AutoMindState) -> AutoMindState:

    question = state.get("question", "").strip()

    history = state.get("history", [])

    rewritten_question = rewrite_question(
        question,
        history=history
    )

    return {
        **state,
        "rewritten_question": rewritten_question,
        "stage": "rewrite",
    }