from services.search_service import search_documents

query = "What projects are mentioned in the resume?"

results = search_documents(
    query,
    limit=100,
)

print()
print("=" * 70)
print("RETRIEVAL RESULTS")
print("=" * 70)
print(f"Total results: {len(results)}")
print()

for index, result in enumerate(results, start=1):
    payload = result.payload or {}

    filename = payload.get(
        "filename",
        "unknown",
    )

    chunk_id = payload.get(
        "chunk_id",
        "unknown",
    )

    score = float(result.score)

    print(
        f"{index:02d}. "
        f"score={score:.4f} | "
        f"file={filename} | "
        f"chunk={chunk_id}"
    )
