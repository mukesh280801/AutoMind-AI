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
        "good afternoon",
        "good evening",
    ]

    smalltalk_exact = [
        "thanks",
        "thank you",
        "ok",
        "okay",
        "bye",
        "goodbye",
        "how are you",
        "how are you doing",
        "how's it going",
        "how is it going",
        "what's up",
        "what is up",
    ]

    # =========================================================
    # Greeting
    # =========================================================

    if question in greetings:
        return "greeting"

    # =========================================================
    # Smalltalk
    # =========================================================

    if question in smalltalk_exact:
        return "smalltalk"

    smalltalk_phrases = [
        "how are you",
        "how are you doing",
        "how's it going",
        "how is it going",
        "what's up",
        "what is up",
    ]

    if any(phrase in question for phrase in smalltalk_phrases):
        return "smalltalk"

    # =========================================================
    # Memory questions
    # =========================================================

    memory_questions = [
        "what is my name",
        "what's my name",
        "do you remember my name",
        "who am i",
        "what project am i working on",
        "what project am i currently working on",
        "what am i working on",
    ]

    if any(memory_question in question for memory_question in memory_questions):
        return "memory"

    # =========================================================
    # Memory statements
    # =========================================================

    memory_statements = [
        "my name is ",
        "i am ",
        "i'm ",
        "you can call me ",
        "my name's ",
        "i work on ",
        "i am working on ",
        "i'm working on ",
    ]

    if any(question.startswith(statement) for statement in memory_statements):
        return "memory"

    # =========================================================
    # Summary
    # =========================================================

    if "summary" in question or "summarize" in question:
        return "summary"

    # =========================================================
    # Comparison
    # =========================================================

    if "compare" in question:
        return "comparison"

    # =========================================================
    # Default
    # =========================================================

    return "search"