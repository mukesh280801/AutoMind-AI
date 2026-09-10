import re
import ollama

from config import OLLAMA_MODEL


NO_DOCUMENT_ANSWER = (
    "I couldn't find that information in the uploaded documents."
)


# ============================================================
# GROUNDED ANSWER SAFEGUARD
# ============================================================

def enforce_grounded_answer(
    question: str,
    context: str,
    answer: str,
) -> str:

    question_lower = question.lower()
    context_lower = context.lower()

    # --------------------------------------------------------
    # Exact fallback normalization
    # --------------------------------------------------------

    fallback_phrases = [
        "there is no employee id",
        "no employee id",
        "employee id is not mentioned",
        "employee id was not mentioned",
        "information is not available",
        "not mentioned in the uploaded documents",
        "not found in the uploaded documents",
        "cannot find that information",
    ]

    if any(
        phrase in answer.lower()
        for phrase in fallback_phrases
    ):
        if "employee id" in question_lower:
            if "employee id" not in context_lower:
                return NO_DOCUMENT_ANSWER

    # --------------------------------------------------------
    # Exact metric extraction
    # --------------------------------------------------------

    metric_patterns = []

    if (
        "f1-score" in question_lower
        or "f1 score" in question_lower
    ):
        metric_patterns = [
            r"(\d+(?:\.\d+)?%?)\s*(?:f1[-\s]?score)",
            r"(?:f1[-\s]?score)[^0-9]{0,20}(\d+(?:\.\d+)?%?)",
        ]

    elif (
        "dice score" in question_lower
        or "dice" in question_lower
    ):
        metric_patterns = [
            r"(\d+(?:\.\d+)?%?)\s*(?:dice\s*score)",
            r"(?:dice\s*score)[^0-9]{0,20}(\d+(?:\.\d+)?%?)",
        ]

    elif "iou" in question_lower:
        metric_patterns = [
            r"(\d+(?:\.\d+)?%?)\s*(?:iou)",
            r"(?:iou)[^0-9]{0,20}(\d+(?:\.\d+)?%?)",
        ]

    elif "accuracy" in question_lower:
        metric_patterns = [
            r"(\d+(?:\.\d+)?%?)\s*(?:accuracy)",
            r"(?:accuracy)[^0-9]{0,20}(\d+(?:\.\d+)?%?)",
        ]

    for pattern in metric_patterns:

        match = re.search(
            pattern,
            context,
            re.IGNORECASE,
        )

        if match:

            exact_value = match.group(1)

            if (
                "f1-score" in question_lower
                or "f1 score" in question_lower
            ):
                return (
                    f"The F1-score is {exact_value}."
                )

            if "dice" in question_lower:
                return (
                    f"The Dice Score is {exact_value}."
                )

            if "iou" in question_lower:
                return (
                    f"The IoU score is {exact_value}."
                )

            if "accuracy" in question_lower:
                return (
                    f"The accuracy is {exact_value}."
                )

    return answer.strip()


# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt(
    context: str,
) -> str:

    return f"""
You are AutoMind AI, a document-based question answering assistant.

Answer the user's question using ONLY the provided document context.

IMPORTANT RULES:

1. Use only information explicitly present in the document context.

2. Never use outside knowledge.

3. Never guess, assume, or infer missing information.

4. Answer exactly what the user asked.

5. Identify the exact entity, project, metric, technology, or fact
   requested by the user before producing the answer.

6. For numerical questions, carefully match the requested metric
   to its corresponding numerical value in the document.

7. NEVER substitute one metric for another.

8. If the question asks for an F1-score, return the F1-score.
   Do not return accuracy, Dice Score, IoU, precision, recall,
   or another metric.

9. If the question asks for accuracy, return the accuracy.
   Do not return F1-score or another metric.

10. If the question asks for Dice Score, return the Dice Score.
    Do not return IoU or another metric.

11. If the question asks for IoU, return the IoU value.
    Do not return Dice Score or another metric.

12. For metric questions, first locate the exact metric name
    requested in the document context and copy the numerical value
    immediately associated with that metric.

    Example:

    "96% accuracy and 0.93 F1-score"

    means:

    Accuracy = 96%
    F1-score = 0.93

    If the user asks for F1-score, the answer MUST contain 0.93.

13. If the question asks for a list, return a concise list.

14. If the question asks "what projects" or "which projects",
    inspect ALL relevant project entries in the provided context.

15. Return every project name explicitly present in the context.

16. Do not return only the first project you find.

17. Do not say "there is only one project" unless the context
    explicitly proves that only one project exists.

18. If multiple projects are present in the context, list all of them.

19. If the question asks for technologies, return the relevant
    technologies/frameworks explicitly mentioned in the context.

20. If the question asks for details about a project, include only
    the relevant description, technologies, and achievements explicitly
    stated in the context.

21. If multiple context sections support the answer, combine them.

22. If the question is a follow-up question referring to a previous
    project or entity, use conversation history only to resolve
    what the reference means. The actual answer must still come from
    the provided document context.

23. If the question is a yes/no question and the context supports
    the answer, answer yes or no and briefly provide evidence.

24. Do not answer a supported yes/no question with only "Yes." or "No."
    when supporting evidence is available.

25. If the requested information is genuinely absent from the context,
    respond EXACTLY:

I couldn't find that information in the uploaded documents.

26. Do not explain why information is missing.

27. Do not fabricate names, dates, scores, projects, technologies,
    achievements, preferences, or any other facts.

DOCUMENT CONTEXT
================

{context}

================
"""


# ============================================================
# NORMAL GENERATION
# ============================================================

def generate_answer(
    question: str,
    context: str,
    history=None,
):

    if history is None:
        history = []

    system_prompt = build_system_prompt(
        context
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages.extend(
        history
    )

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        options={
            "temperature": 0,
        },
    )

    answer = response[
        "message"
    ].get(
        "content",
        "",
    )

    if not answer:
        return NO_DOCUMENT_ANSWER

    answer = answer.strip()

    # --------------------------------------------------------
    # Grounding safeguard
    # --------------------------------------------------------

    answer = enforce_grounded_answer(
        question=question,
        context=context,
        answer=answer,
    )

    return answer


# ============================================================
# STREAMING GENERATION
# ============================================================

def generate_answer_stream(
    question: str,
    context: str,
    history=None,
):

    if history is None:
        history = []

    system_prompt = build_system_prompt(
        context
    )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages.extend(
        history
    )

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    stream = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        stream=True,
        options={
            "temperature": 0,
        },
    )

    for chunk in stream:

        content = (
            chunk[
                "message"
            ].get(
                "content",
                "",
            )
        )

        if content:
            yield content