import requests

url = "http://127.0.0.1:8000/api/v2/chat/stream"

payload = {
    "question": "What projects has Mukesh worked on and explain each project briefly?",
    "thread_id": "stream_005",
}

print("Starting stream...\n")

with requests.post(url, json=payload, stream=True) as response:

    print("Status:", response.status_code)
    print("Response:\n")

    for chunk in response.iter_content(
        chunk_size=None,
        decode_unicode=True
    ):
        if chunk:
            print(chunk, end="", flush=True)

print("\n\nStream finished.")