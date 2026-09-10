def split_text(text: str, chunk_size: int = 500):
    chunks = []

    # Split primarily by sections/paragraphs instead of
    # cutting blindly at every N characters.
    sections = text.split("\n")

    current_chunk = ""

    for section in sections:
        section = section.strip()

        if not section:
            continue

        if len(current_chunk) + len(section) + 1 <= chunk_size:
            current_chunk += section + "\n"
        else:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            current_chunk = section + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks