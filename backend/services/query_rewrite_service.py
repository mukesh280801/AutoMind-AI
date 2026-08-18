from services.memory_service import get_history


def rewrite_question(question: str):

    history = get_history()

    # No previous conversation
    if not history:
        return question

    # Find the previous user question
    previous_user = ""

    for message in reversed(history):
        if message["role"] == "user":
            previous_user = message["content"]
            break

    # No previous user question
    if not previous_user:
        return question

    # Follow-up indicators
    follow_up_words = [
        "it",
        "this",
        "that",
        "these",
        "those",
        "he",
        "she",
        "they",
        "his",
        "her",
        "their",
        "also",
        "more",
        "what about",
        "how about",
        "and"
    ]

    question_lower = question.lower().strip()

    # Rewrite only when the new question appears
    # to depend on the previous question.
    is_follow_up = any(
        question_lower.startswith(word + " ")
        or question_lower == word
        for word in follow_up_words
    )

    if is_follow_up:
        return (
            f"Previous question: {previous_user}\n"
            f"Follow-up question: {question}"
        )

    # Independent question → keep it unchanged
    return question