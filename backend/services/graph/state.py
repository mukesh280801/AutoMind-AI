from typing import TypedDict, List


class AutoMindState(TypedDict, total=False):

    question: str
    thread_id: str
    request_id: str

    intent: str

    rewritten_question: str

    retrieved_chunks: List[str]

    retrieval_scores: List[float]

    retrieval_sources: List[dict]

    retrieval_found: bool

    compressed_context: str

    answer: str

    history: List[dict]

    stage: str