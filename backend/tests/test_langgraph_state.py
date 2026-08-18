from services.graph.state import AutoMindState


state: AutoMindState = {
    "question": "What projects has Mukesh worked on?",
    "intent": "search",
}

print("\n==============================")
print("LANGGRAPH STATE TEST")
print("==============================")

print("Question:", state["question"])
print("Intent:", state["intent"])

print("==============================")
print("State created successfully")