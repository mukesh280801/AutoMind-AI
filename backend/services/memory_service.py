from config import MAX_HISTORY

conversation_history = []


def add_message(role: str, content: str):

    conversation_history.append({
        "role": role,
        "content": content
    })

    # Keep only recent messages
    if len(conversation_history) > MAX_HISTORY:
        conversation_history.pop(0)


def get_history():
    return conversation_history


def clear_history():
    conversation_history.clear()