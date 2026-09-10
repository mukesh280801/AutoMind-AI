def compress_context(question: str, chunks: list[str]) -> str:
    """
    Compress and organize retrieved context.

    For broad list/section queries, preserve all retrieved chunks
    because coverage is more important than aggressive filtering.

    For normal queries, rank chunks using simple keyword overlap
    while still preserving all retrieved information.
    """

    if not chunks:
        return ""

    question_words = {
        word.lower().strip(".,?!:;()[]{}")
        for word in question.split()
        if len(word.strip(".,?!:;()[]{}")) > 2
    }

    scored_chunks = []

    for index, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()

        score = sum(
            1
            for word in question_words
            if word in chunk_lower
        )

        scored_chunks.append(
            (score, index, chunk)
        )

    question_lower = question.lower()

    is_list_query = (
        "what projects" in question_lower
        or "which projects" in question_lower
        or "list the projects" in question_lower
        or "projects has" in question_lower
        or "projects did" in question_lower
    )

    if is_list_query:
        # Preserve retrieval order for broad list queries.
        # This prevents important project chunks from being
        # buried by keyword reordering.
        selected_chunks = chunks

    else:
        # Rank normal queries by keyword relevance.
        scored_chunks.sort(
            key=lambda item: (-item[0], item[1])
        )

        selected_chunks = [
            chunk
            for score, index, chunk in scored_chunks
        ]

    return "\n\n".join(selected_chunks)