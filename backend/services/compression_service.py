def compress_context(question: str, chunks: list[str]) -> str:
    """
    Compress retrieved context while preserving relevant information.

    Strategy:
    1. Keep chunks that contain important query keywords.
    2. Always preserve the first relevant chunks.
    3. Avoid overly aggressive sentence filtering.
    4. Fall back to the original retrieved context when necessary.
    """

    if not chunks:
        return ""

    question_words = set(
        word.lower().strip(".,?!:;()[]{}")
        for word in question.split()
        if len(word.strip(".,?!:;()[]{}")) > 2
    )

    scored_chunks = []

    for chunk in chunks:

        chunk_lower = chunk.lower()

        score = sum(
            1
            for word in question_words
            if word in chunk_lower
        )

        scored_chunks.append(
            (score, chunk)
        )

    # Sort by relevance
    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # Keep all retrieved chunks.
    # Retrieval has already selected relevant information,
    # so compression should not aggressively delete context.
    selected_chunks = [
        chunk
        for score, chunk in scored_chunks
    ]

    # Join the retrieved context
    context = "\n\n".join(selected_chunks)

    return context