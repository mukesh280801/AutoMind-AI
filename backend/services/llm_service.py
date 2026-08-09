import ollama

from config import OLLAMA_MODEL


# ============================================================
# Generate Answer
# ============================================================

def generate_answer(
    question: str,
    context: str,
    history=None
):
    """
    Generate a grounded response from the LLM.

    The LLM must answer only from facts explicitly
    supported by the retrieved context.
    """

    if history is None:
        history = []

    system_prompt = f"""
You are AutoMind AI, a document-based question answering assistant.

Your job is to answer the user's question using ONLY the
information explicitly present in the provided context.

STRICT GROUNDING RULES:

1. Use ONLY facts explicitly stated in the context.

2. Do NOT use outside knowledge.

3. Do NOT guess, assume, or infer information.

4. A related fact is NOT enough to answer the question.

   Example:
   If the context says:
   "Python is one of Mukesh's programming languages."

   And the user asks:
   "What is Mukesh's favorite programming language?"

   You MUST NOT answer "Python".

   The context does not explicitly say that Python is his favorite.

5. If the context does not explicitly contain the answer,
   respond ONLY with:

   "I couldn't find that information in the uploaded documents."

6. Do not add an explanation after saying the information
   was not found.

7. Do not fabricate names, dates, scores, projects,
   technologies, achievements, preferences, or other facts.

8. When the context contains the answer, give a concise
   answer based only on that context.

Context:
--------------------
{context}
--------------------
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Previous conversation
    messages.extend(history)

    # Current question
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages
    )

    return response["message"]["content"]


# ============================================================
# Streaming Answer
# ============================================================

def generate_answer_stream(
    question: str,
    context: str,
    history=None
):
    """
    Stream a grounded response from the LLM token by token.
    """

    if history is None:
        history = []

    system_prompt = f"""
You are AutoMind AI, a document-based question answering assistant.

Answer the user's question using ONLY information explicitly
present in the provided context.

STRICT GROUNDING RULES:

1. Use only facts explicitly stated in the context.

2. Never use outside knowledge.

3. Never guess or infer missing information.

4. Do not treat a related fact as proof of the requested fact.

5. If the context does not explicitly answer the question,
   respond ONLY with:

   "I couldn't find that information in the uploaded documents."

6. Do not add any additional information after saying
   the information was not found.

7. Do not fabricate facts.

Context:
--------------------
{context}
--------------------
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Previous conversation
    messages.extend(history)

    # Current question
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    stream = ollama.chat(
        model=OLLAMA_MODEL,
        messages=messages,
        stream=True
    )

    for chunk in stream:

        content = chunk["message"].get(
            "content",
            ""
        )

        if content:
            yield content