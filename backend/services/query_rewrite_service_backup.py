from services.memory_service import get_history


def rewrite_question(
    question: str,
):

    history = get_history()

    if not history:
        return question

    previous_user = ""

    for message in reversed(history):

        if message.get(
            "role"
        ) == "user":

            previous_user = (
                message.get(
                    "content",
                    "",
                )
            )

            break

    if not previous_user:
        return question

    question_lower = question.lower()

    # =========================================================
    # Explicit follow-up questions
    # =========================================================

    follow_up_words = [
        "what about",
        "what is",
        "what are",
        "how about",
        "which one",
        "which ones",
        "tell me more",
    ]

    is_follow_up = any(
        word in question_lower
        for word in follow_up_words
    )

    if is_follow_up:

        return (
            f"{question} "
            f"{previous_user}"
        )

    return question