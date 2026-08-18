from services.graph.workflow import build_graph


graph = build_graph()

initial_state = {
    "question": "What projects has Mukesh worked on?"
}

config = {
    "configurable": {
        "thread_id": "test-memory"
    }
}

result = graph.invoke(
    initial_state,
    config=config,
)

print("\n==============================")
print("LANGGRAPH MEMORY TEST")
print("==============================")

print("Question:")
print(result["question"])

print("\nHistory messages:")
print(len(result.get("history", [])))

for message in result.get("history", []):
    print(message)

print("\nAnswer:")
print(result["answer"])

print("\n==============================")