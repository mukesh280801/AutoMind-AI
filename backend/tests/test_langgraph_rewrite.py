from services.graph.workflow import build_graph


graph = build_graph()

initial_state = {
    "question": "What projects has Mukesh worked on?"
}

config = {
    "configurable": {
        "thread_id": "test-rewrite"
    }
}

result = graph.invoke(
    initial_state,
    config=config,
)

print("\n==============================")
print("LANGGRAPH REWRITE TEST")
print("==============================")

print("Original question:")
print(result["question"])

print("\nIntent:")
print(result["intent"])

print("\nRewritten question:")
print(result["rewritten_question"])

print("==============================")