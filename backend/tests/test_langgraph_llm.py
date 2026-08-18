from services.graph.workflow import build_graph


graph = build_graph()

initial_state = {
    "question": "Which project used Attention U-Net?"
}

config = {
    "configurable": {
        "thread_id": "test-llm"
    }
}

result = graph.invoke(
    initial_state,
    config=config,
)

print("\n==============================")
print("LANGGRAPH LLM TEST")
print("==============================")

print("Question:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\n==============================")