from services.graph.workflow import build_graph


graph = build_graph()


config = {
    "configurable": {
        "thread_id": "test_conversation_001"
    }
}


print("\n==============================")
print("LANGGRAPH CHECKPOINT TEST")
print("==============================")


# First question
state_1 = graph.invoke(
    {
        "question": "What projects has Mukesh worked on?"
    },
    config=config
)

print("\nFirst question:")
print(state_1["question"])

print("\nFirst answer:")
print(state_1["answer"])


# Follow-up question using SAME thread
state_2 = graph.invoke(
    {
        "question": "Which one used Attention U-Net?"
    },
    config=config
)

print("\nFollow-up question:")
print(state_2["question"])

print("\nFollow-up answer:")
print(state_2["answer"])


print("\n==============================")
print("CHECKPOINT TEST COMPLETE")
print("==============================")