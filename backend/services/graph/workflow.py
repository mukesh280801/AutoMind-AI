import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from services.graph.state import AutoMindState
from services.graph.memory_node import memory_node
from services.graph.intent_node import intent_node
from services.graph.router import (
    route_after_intent,
    route_after_retrieval,
)
from services.graph.rewrite_node import rewrite_node
from services.graph.retrieval_node import retrieval_node
from services.graph.compression_node import compression_node
from services.graph.llm_node import llm_node
from services.graph.response_node import response_node


connection = sqlite3.connect(
    "automind_checkpoints.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(connection)


def build_graph():

    graph = StateGraph(AutoMindState)

    graph.add_node("memory", memory_node)
    graph.add_node("intent", intent_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("compression", compression_node)
    graph.add_node("llm", llm_node)
    graph.add_node("response", response_node)

    # =========================================================
    # Start
    # =========================================================

    graph.add_edge(START, "memory")

    graph.add_edge("memory", "intent")

    # =========================================================
    # Intent routing
    # =========================================================

    graph.add_conditional_edges(
        "intent",
        route_after_intent,
        {
            "response": "response",
            "rewrite": "rewrite",
        },
    )

    # =========================================================
    # Search path
    # =========================================================

    graph.add_edge(
        "rewrite",
        "retrieval",
    )

    graph.add_conditional_edges(
        "retrieval",
        route_after_retrieval,
        {
            "compression": "compression",
            "response": "response",
        },
    )

    graph.add_edge(
        "compression",
        "llm",
    )

    graph.add_edge(
        "llm",
        END,
    )

    # =========================================================
    # Direct response path
    # =========================================================

    graph.add_edge("response", END)

    # =========================================================
    # Compile
    # =========================================================

    return graph.compile(
        checkpointer=checkpointer,
    )