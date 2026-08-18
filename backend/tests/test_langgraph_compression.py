from services.graph.workflow import build_graph


graph = build_graph()


initial_state = {
    "question": "Which project used Attention U-Net?"
}


config = {
    "configurable": {
        "thread_id": "test-compression"
    }
}


result = graph.invoke(
    initial_state,
    config=config,
)


print("\n==============================")
print("LANGGRAPH COMPRESSION TEST")
print("==============================")

print("Question:")
print(result["question"])

print("\nIntent:")
print(result["intent"])

print("\nRetrieved chunks:")
print(len(result["retrieved_chunks"]))

print("\nCompressed context:")
print(result["compressed_context"])

print("\n==============================")