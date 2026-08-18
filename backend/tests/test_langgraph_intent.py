from services.graph.workflow import build_graph


graph = build_graph()


initial_state = {
    "question": "What projects has Mukesh worked on?"
}


config = {
    "configurable": {
        "thread_id": "test-intent"
    }
}


result = graph.invoke(
    initial_state,
    config=config,
)


print("\n==============================")
print("LANGGRAPH INTENT TEST")
print("==============================")

print("Question:", result["question"])
print("Detected intent:", result["intent"])

print("==============================")