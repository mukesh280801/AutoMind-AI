from services.graph.workflow import build_graph


# =========================================================
# Build LangGraph
# =========================================================

graph = build_graph()


# =========================================================
# Graph Configuration
# =========================================================

def get_graph_config(thread_id: str):
    """
    Create LangGraph configuration for a conversation thread.

    thread_id is used by the checkpointer to maintain
    isolated conversation state.
    """

    return {
        "configurable": {
            "thread_id": thread_id
        }
    }


# =========================================================
# NORMAL V2 CHAT
# =========================================================

def process_graph_chat(
    question: str,
    thread_id: str = "default",
):
    """
    Execute the LangGraph once and return the final state.
    """

    config = get_graph_config(thread_id)

    result = graph.invoke(
        {
            "question": question,
            "request_id": thread_id,
        },
        config=config,
    )

    return result


# =========================================================
# STREAMING V2 CHAT
# =========================================================

def stream_graph_chat(
    question: str,
    thread_id: str = "default",
):
    """
    Execute the V2 LangGraph once and stream the final answer.

    Important:
    The graph itself is executed only once.

    We intentionally use graph.invoke() here instead of trying
    to reconstruct Ollama token streaming through LangGraph.
    This keeps the normal V2 grounding, memory, retrieval,
    compression and response logic unchanged.
    """

    config = get_graph_config(thread_id)

    # =====================================================
    # Execute graph exactly once
    # =====================================================

    result = graph.invoke(
        {
            "question": question,
            "request_id": thread_id,
        },
        config=config,
    )

    # =====================================================
    # Get final answer
    # =====================================================

    answer = result.get(
        "answer",
        "",
    )

    if not answer:
        answer = (
            "I couldn't generate an answer from "
            "the uploaded documents."
        )

    answer = str(answer).strip()

    if not answer:
        return

    # =====================================================
    # Stream answer in small chunks
    # =====================================================
    #
    # This gives the API streaming behaviour without
    # executing the LangGraph or LLM twice.
    #

    chunk_size = 40

    for start in range(
        0,
        len(answer),
        chunk_size,
    ):
        yield answer[
            start:start + chunk_size
        ]