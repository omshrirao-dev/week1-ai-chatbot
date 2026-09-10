import requests

response = requests.post(
    "http://127.0.0.1:8000/chat/stream",
    json={"message": "explain what is RAG in AI in detail"},
    stream=True
)

print("Streaming response:\n")
for chunk in response.iter_content(chunk_size=None):
    if chunk:
        print(chunk.decode("utf-8"), end="", flush=True)

print("\n\nDone.")