from services.graph.state import AutoMindState
from services.logging_service import get_logger


logger = get_logger("automind.graph.response")


# =========================================================
# RESPONSE NODE
# =========================================================

def response_node(state: AutoMindState) -> AutoMindState:
    """
    Generate direct responses for:
    - greeting
    - smalltalk
    - memory

    The current user message and assistant response are
    appended to the LangGraph checkpointed history.
    """

    intent = state.get("intent", "")
    request_id = state.get("request_id", "unknown")
    question = state.get("question", "")
    history = state.get("history", [])

    # =====================================================
    # Generate response
    # =====================================================

    if intent == "greeting":

        answer = "Hello! How can I help you?"

    elif intent == "smalltalk":

        answer = "I'm doing well, thanks for asking!"

    elif intent == "memory":

        answer = _answer_from_memory(
            question,
            history,
        )

    else:

        answer = (
            "I couldn't find that information "
            "in the uploaded documents."
        )

    # =====================================================
    # Update conversation history
    # =====================================================

    updated_history = history + [
        {
            "role": "user",
            "content": question,
        },
        {
            "role": "assistant",
            "content": answer,
        },
    ]

    # =====================================================
    # Logging
    # =====================================================

    logger.info(
        "stage=response | request_id=%s | intent=%s | answer_chars=%d",
        request_id,
        intent,
        len(answer),
    )

    logger.info(
        "stage=response | request_id=%s | history_messages=%d",
        request_id,
        len(updated_history),
    )

    # =====================================================
    # Return updated state
    # =====================================================

    return {
        **state,
        "answer": answer,
        "history": updated_history,
        "stage": "response",
    }


# =========================================================
# MEMORY ANSWER
# =========================================================

def _answer_from_memory(
    question: str,
    history: list[dict],
) -> str:
    """
    Answer supported memory questions from conversation history.

    Supports:
    - User name
    - Current project
    - Combined name + project questions
    """

    question_lower = (
        question
        .lower()
        .strip()
    )

    # =====================================================
    # What is the user asking for?
    # =====================================================

    asks_name = (
        "what is my name" in question_lower
        or "what's my name" in question_lower
        or "do you remember my name" in question_lower
        or "who am i" in question_lower
    )

        # =====================================================
    # MEMORY STATEMENTS
    # =====================================================

    if question_lower.startswith("my name is "):

        name = question[11:].strip().rstrip(".,!?").strip()

        if name:
            return f"Nice to meet you, {name}. I'll remember that."

    if question_lower.startswith("my name's "):

        name = question[10:].strip().rstrip(".,!?").strip()

        if name:
            return f"Nice to meet you, {name}. I'll remember that."

    if question_lower.startswith("you can call me "):

        name = question[16:].strip().rstrip(".,!?").strip()

        if name:
            return f"Got it. I'll remember that you prefer to be called {name}."

    # =====================================================
    # PROJECT MEMORY STATEMENT
    # =====================================================

    project_markers = [
        "i am working on ",
        "i'm working on ",
        "i work on ",
    ]

    for marker in project_markers:

        if question_lower.startswith(marker):

            project = question[len(marker):].strip()

            project = project.rstrip(".,!?").strip()

            if project:
                return (
                    f"Got it. I'll remember that you're "
                    f"working on {project}."
                )

    asks_project = (
        "what project am i working on"
        in question_lower
        or "what project am i currently working on"
        in question_lower
        or "what am i working on"
        in question_lower
    )

    # =====================================================
    # Combined question
    # =====================================================

    if asks_name and asks_project:

        name = _find_user_name(history)
        project = _find_user_project(history)

        answers = []

        if name:
            answers.append(
                f"Your name is {name}."
            )

        if project:
            answers.append(
                f"You are working on {project}."
            )

        if answers:
            return "\n".join(answers)

        return (
            "I don't have your name or project "
            "information in our conversation history."
        )

    # =====================================================
    # Name question
    # =====================================================

    if asks_name:

        name = _find_user_name(history)

        if name:
            return f"Your name is {name}."

        return (
            "I don't have your name "
            "in our conversation history."
        )

    # =====================================================
    # Project question
    # =====================================================

    if asks_project:

        project = _find_user_project(history)

        if project:
            return (
                f"You are working on {project}."
            )

        return (
            "I don't have your project information "
            "in our conversation history."
        )

    # =====================================================
    # Generic memory
    # =====================================================

    if history:

        return (
            "I remember our previous conversation, "
            "but I don't have a specific stored answer "
            "for that question."
        )

    return (
        "I don't have any previous conversation "
        "history for that question."
    )


# =========================================================
# FIND USER NAME
# =========================================================

def _find_user_name(
    history: list[dict],
) -> str | None:
    """
    Search conversation history for an explicit
    user-name statement.

    Supported:

        My name is Mukesh.
        I'm Mukesh.
        I am Mukesh.
        My name's Mukesh.
        You can call me Mukesh.

    IMPORTANT:
        "I am working on AutoMind AI"
        must NOT become a name.
    """

    for message in reversed(history):

        if message.get("role") != "user":
            continue

        content = (
            message.get("content", "")
            .strip()
        )

        if not content:
            continue

        content_lower = content.lower()

        # =================================================
        # My name is X
        # =================================================

        marker = "my name is "

        if content_lower.startswith(marker):

            name = content[len(marker):].strip()

            name = _clean_value(name)

            if name and _looks_like_name(name):

                return name

        # =================================================
        # I'm X
        # =================================================

        marker = "i'm "

        if content_lower.startswith(marker):

            value = content[len(marker):].strip()

            value = _clean_value(value)

            if (
                value
                and not _looks_like_project_statement(value)
                and _looks_like_name(value)
            ):

                return value

        # =================================================
        # I am X
        # =================================================

        marker = "i am "

        if content_lower.startswith(marker):

            value = content[len(marker):].strip()

            value = _clean_value(value)

            if (
                value
                and not _looks_like_project_statement(value)
                and _looks_like_name(value)
            ):

                return value

        # =================================================
        # My name's X
        # =================================================

        marker = "my name's "

        if content_lower.startswith(marker):

            name = content[len(marker):].strip()

            name = _clean_value(name)

            if name and _looks_like_name(name):

                return name

        # =================================================
        # You can call me X
        # =================================================

        marker = "you can call me "

        if content_lower.startswith(marker):

            name = content[len(marker):].strip()

            name = _clean_value(name)

            if name and _looks_like_name(name):

                return name

    return None


# =========================================================
# FIND USER PROJECT
# =========================================================

def _find_user_project(
    history: list[dict],
) -> str | None:
    """
    Search conversation history for an explicit
    project statement.

    Supported:

        I am working on an AI project called AutoMind AI.
        I'm working on AutoMind AI.
        I am working on AutoMind AI.
        I work on AutoMind AI.
        My project is AutoMind AI.
        Project called AutoMind AI.
    """

    for message in reversed(history):

        if message.get("role") != "user":
            continue

        content = (
            message.get("content", "")
            .strip()
        )

        if not content:
            continue

        content_lower = content.lower()

        # =================================================
        # I am working on an AI project called X
        # =================================================

        marker = "i am working on an ai project called "

        if marker in content_lower:

            start = (
                content_lower.index(marker)
                + len(marker)
            )

            project = content[start:].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # I'm working on an AI project called X
        # =================================================

        marker = "i'm working on an ai project called "

        if marker in content_lower:

            start = (
                content_lower.index(marker)
                + len(marker)
            )

            project = content[start:].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # Project called X
        # =================================================

        marker = "project called "

        if marker in content_lower:

            start = (
                content_lower.index(marker)
                + len(marker)
            )

            project = content[start:].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # I'm working on X
        # =================================================

        marker = "i'm working on "

        if content_lower.startswith(marker):

            project = content[len(marker):].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # I am working on X
        # =================================================

        marker = "i am working on "

        if content_lower.startswith(marker):

            project = content[len(marker):].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # I work on X
        # =================================================

        marker = "i work on "

        if content_lower.startswith(marker):

            project = content[len(marker):].strip()

            project = _clean_value(project)

            if project:
                return project

        # =================================================
        # My project is X
        # =================================================

        marker = "my project is "

        if content_lower.startswith(marker):

            project = content[len(marker):].strip()

            project = _clean_value(project)

            if project:
                return project

    return None


# =========================================================
# CLEAN VALUE
# =========================================================

def _clean_value(
    value: str,
) -> str:
    """
    Remove common trailing punctuation.
    """

    value = value.strip()

    value = value.rstrip(
        ".,!?"
    )

    return value.strip()


# =========================================================
# NAME VALIDATION
# =========================================================

def _looks_like_name(
    value: str,
) -> bool:
    """
    Prevent project/work statements from being
    interpreted as names.
    """

    value_lower = (
        value
        .lower()
        .strip()
    )

    blocked_starts = [
        "working on ",
        "working with ",
        "working at ",
        "building ",
        "developing ",
        "creating ",
        "using ",
        "studying ",
        "an ai project ",
        "a project ",
        "project ",
    ]

    for prefix in blocked_starts:

        if value_lower.startswith(prefix):

            return False

    return True


# =========================================================
# PROJECT STATEMENT DETECTION
# =========================================================

def _looks_like_project_statement(
    value: str,
) -> bool:
    """
    Detect values that clearly describe
    project/work activity.
    """

    value_lower = (
        value
        .lower()
        .strip()
    )

    project_phrases = [
        "working on ",
        "working with ",
        "working at ",
        "project ",
        "an ai project ",
        "a project ",
        "building ",
        "developing ",
        "creating ",
        "using ",
        "studying ",
    ]

    return any(
        value_lower.startswith(phrase)
        for phrase in project_phrases
    )