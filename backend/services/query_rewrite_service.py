from services.memory_service import get_history


def rewrite_question(question: str):

    history = get_history()

    # No previous conversation
    if not history:
        return question

    # Last user message
    previous_user = ""

    for message in reversed(history):
        if message["role"] == "user":
            previous_user = message["content"]
            break

    if previous_user:
        return f"{previous_user}\nFollow-up question: {question}"

    return question