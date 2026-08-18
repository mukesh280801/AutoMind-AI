from services.graph.workflow import build_graph
from services.memory_service import add_message


graph = build_graph()

# Simulate previous conversation
add_message(
    "user",
    "What projects has Mukesh worked on?"
)

add_message(
    "assistant",
    "Mukesh has worked on two projects: Brain Tumor Segmentation and Lung Disease Detection."
)

initial_state = {
    "question": "Which one used Attention U-Net?"
}

config = {
    "configurable": {
        "thread_id": "test-conversation"
    }
}

result = graph.invoke(
    initial_state,
    config=config,
)

print("\n==============================")
print("LANGGRAPH CONVERSATION TEST")
print("==============================")

print("Question:")
print(result["question"])

print("\nHistory messages:")
print(len(result.get("history", [])))

print("\nAnswer:")
print(result["answer"])

print("\n==============================")