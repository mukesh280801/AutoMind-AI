from config import DEFAULT_TOP_K


# Number of chunks to retrieve for each intent
INTENT_TOP_K = {
    "summary": 6,
    "comparison": 5,
    "search": 6,
}


def get_top_k(intent: str) -> int:
    """
    Return the number of document chunks to retrieve
    based on the detected intent.
    """

    return INTENT_TOP_K.get(
        intent,
        DEFAULT_TOP_K
    )