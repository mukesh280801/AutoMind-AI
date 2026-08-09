def detect_intent(question: str) -> str:
    """
    Detect the type of user query.
    """

    question = question.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good evening"
    ]

    thanks = [
        "thanks",
        "thank you",
        "ok",
        "bye"
    ]

    if question in greetings:
        return "greeting"

    if question in thanks:
        return "smalltalk"

    if "summary" in question or "summarize" in question:
        return "summary"

    if "compare" in question:
        return "comparison"

    return "search"