from services.graph.workflow import build_graph


graph = build_graph()

initial_state = {
    "question": "What projects has Mukesh worked on?"
}

config = {
    "configurable": {
        "thread_id": "test-retrieval"
    }
}

result = graph.invoke(
    initial_state,
    config=config,
)

print("\n==============================")
print("LANGGRAPH RETRIEVAL TEST")
print("==============================")

print("Question:")
print(result["question"])

print("\nIntent:")
print(result["intent"])

print("\nRewritten:")
print(result["rewritten_question"])

print("\nRetrieved chunks:")
print(len(result.get("retrieved_chunks", [])))

for i, chunk in enumerate(result.get("retrieved_chunks", []), 1):
    print(f"\n--- CHUNK {i} ---")
    print(chunk[:500])

print("\n==============================")