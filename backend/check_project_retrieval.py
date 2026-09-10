from services.search_service import search_documents


queries = [
    "What is the Dice Score of the Attention U-Net project?",
    """Previous question: What is the Dice Score of the Attention U-Net project?
Follow-up question: What was the IoU score of that project?""",
]


for query in queries:

    print()
    print("=" * 80)
    print("QUERY")
    print("=" * 80)
    print(query)

    results = search_documents(query, limit=6)

    print()
    print(f"Retrieved chunks: {len(results)}")

    for i, result in enumerate(results, start=1):

        payload = result.payload or {}

        print()
        print("-" * 80)
        print(f"RESULT {i}")
        print("-" * 80)

        print(
            f"Score    : {float(result.score):.4f}"
        )

        print(
            f"Filename : {payload.get('filename')}"
        )

        print(
            f"Chunk ID : {payload.get('chunk_id')}"
        )

        print()
        print("TEXT:")
        print(
            payload.get("text", "")
        )