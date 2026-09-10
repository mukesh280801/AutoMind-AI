from services.graph.workflow import build_graph
from services.llm_service import generate_answer_stream


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
# TRUE STREAMING V2 CHAT
# =========================================================

def stream_graph_chat(
    question: str,
    thread_id: str = "default",
):
    """
    Run the V2 RAG graph up to the compression stage and
    then stream the answer directly from Ollama.

    Search flow:

        Memory
          ↓
        Intent
          ↓
        Rewrite
          ↓
        Retrieval
          ↓
        Compression
          ↓
        Ollama stream=True
          ↓
        Tokens

    The function yields dictionaries so the API layer can
    send both answer tokens and source metadata.
    """

    config = get_graph_config(thread_id)

    final_state = None

    # =====================================================
    # Run graph until compression
    # =====================================================

    for state in graph.stream(
        {
            "question": question,
            "request_id": thread_id,
        },
        config=config,
        stream_mode="values",
    ):
        final_state = state

        # Stop before normal LLM node generates
        # the complete answer.
        if state.get("stage") == "compression":
            break

        # Direct-response path such as greeting/smalltalk
        # does not go through compression.
        if state.get("stage") == "response":
            answer = str(
                state.get("answer", "")
            ).strip()

            sources = state.get(
                "retrieval_sources",
                [],
            )

            yield {
                "type": "sources",
                "sources": sources,
            }

            if answer:
                yield {
                    "type": "token",
                    "content": answer,
                }

            yield {
                "type": "done",
            }

            return

    # =====================================================
    # Safety check
    # =====================================================

    if not final_state:
        yield {
            "type": "error",
            "content": (
                "I couldn't generate an answer from "
                "the uploaded documents."
            ),
        }
        return

    # =====================================================
    # Get retrieval sources
    # =====================================================

    sources = final_state.get(
        "retrieval_sources",
        [],
    )

    yield {
        "type": "sources",
        "sources": sources,
    }

    # =====================================================
    # Get RAG context
    # =====================================================

    context = final_state.get(
        "compressed_context",
        "",
    )

    retrieved_chunks = final_state.get(
        "retrieved_chunks",
        [],
    )

    history = final_state.get(
        "history",
        [],
    )

    # =====================================================
    # No retrieved information
    # =====================================================

    if not retrieved_chunks or not context:
        answer = (
            "I couldn't find that information in "
            "the uploaded documents."
        )

        yield {
            "type": "token",
            "content": answer,
        }

        yield {
            "type": "done",
        }

        return

    # =====================================================
    # True Ollama token streaming
    # =====================================================

    try:
        for token in generate_answer_stream(
            question=question,
            context=context,
            history=history,
        ):
            yield {
                "type": "token",
                "content": token,
            }

    except Exception:
        yield {
            "type": "error",
            "content": (
                "I couldn't generate an answer from "
                "the uploaded documents."
            ),
        }

        return

    # =====================================================
    # Streaming completed
    # =====================================================

    yield {
        "type": "done",
    }