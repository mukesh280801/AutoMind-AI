from services.graph.workflow import build_graph


graph = build_graph()


config = {
    "configurable": {
        "thread_id": "router_test_001"
    }
}


print("\n==============================")
print("LANGGRAPH ROUTING TEST")
print("==============================")


# Test 1: Greeting

result = graph.invoke(
    {
        "question": "hello"
    },
    config=config
)

print("\nTest 1")
print("Question:", result["question"])
print("Intent:", result["intent"])
print("Answer:", result.get("answer", "No LLM call"))


# Test 2: Search

result = graph.invoke(
    {
        "question": "What projects has Mukesh worked on?"
    },
    config={
        "configurable": {
            "thread_id": "router_test_002"
        }
    }
)

print("\nTest 2")
print("Question:", result["question"])
print("Intent:", result["intent"])
print("Answer:", result.get("answer", ""))


print("\n==============================")
print("ROUTING TEST COMPLETE")
print("==============================")