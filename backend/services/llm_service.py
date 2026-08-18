import ollama

from config import OLLAMA_MODEL


NO_DOCUMENT_ANSWER = (
    "I couldn't find that information in the uploaded documents."
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

def build_system_prompt(
    context: str,
) -> str:

    return f"""
You are AutoMind AI.

You are a document question-answering assistant.

Your answer MUST be based ONLY on the provided document context.

IMPORTANT RULES:

1. Read the entire context before answering.

2. Answer the user's CURRENT question.

3. Use only facts explicitly present in the context.

4. Do not use outside knowledge.

5. Do not invent information.

6. Do not guess.

7. Do not infer facts that are not explicitly supported.

8. If the question asks about projects, list the projects
   explicitly mentioned in the context.

9. If multiple project sections appear in the context,
   combine them into one concise answer.

10. If technologies are mentioned under a project,
    include them only when they help answer the question.

11. If the context does not contain information that directly
    answers the question, respond EXACTLY:

I couldn't find that information in the uploaded documents.

12. Do not explain why information was missing.

13. Do not mention the retrieval system, Qdrant, embeddings,
    context, prompt, or internal pipeline.

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

    # --------------------------------------------------------
    # IMPORTANT
    # --------------------------------------------------------
    # History can sometimes contain previous answers that
    # confuse document grounding.
    #
    # For now we keep it, but the system prompt tells the
    # model to answer the CURRENT question from documents.
    # --------------------------------------------------------

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
    )

    answer = response[
        "message"
    ].get(
        "content",
        "",
    )

    if not answer:

        return NO_DOCUMENT_ANSWER

    return answer.strip()


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