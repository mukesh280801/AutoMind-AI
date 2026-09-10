def rewrite_question(question: str, history=None):
    """
    Rewrite a follow-up question using LangGraph conversation history.

    Independent questions are returned unchanged.

    Follow-up questions containing explicit references such as
    "that project" or "this project" are expanded with the
    previous user question so retrieval has enough context.
    """

    if history is None:
        history = []

    # No previous conversation
    if not history:
        return question

    # Find the most recent user question
    previous_user = ""

    for message in reversed(history):
        if message.get("role") == "user":
            previous_user = message.get("content", "").strip()
            break

    # No previous user question
    if not previous_user:
        return question

    question_lower = question.lower().strip()

    # Explicit follow-up references
    follow_up_phrases = [
        "that project",
        "this project",
        "the project",
        "that one",
        "this one",
        "what about",
        "how about",
        "also",
    ]

    is_follow_up = any(
        phrase in question_lower
        for phrase in follow_up_phrases
    )

    if is_follow_up:
        return (
            f"Previous question: {previous_user}\n"
            f"Follow-up question: {question}"
        )

    # Independent question
    return question