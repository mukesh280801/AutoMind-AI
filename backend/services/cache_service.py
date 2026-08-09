# Simple in-memory cache

cache = {}


def get_cached_answer(question: str):
    """
    Return cached answer if available.
    """
    return cache.get(question.lower())


def save_cached_answer(question: str, answer: str):
    """
    Save answer into cache.
    """
    cache[question.lower()] = answer