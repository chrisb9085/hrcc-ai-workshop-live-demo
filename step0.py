import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b-instruct"

messages = [
    {"role": "user", "content": "What is 250 US dollars in Euros right now?"}
]

response = requests.post(
    OLLAMA_URL,
    json={"model": MODEL, "messages": messages, "stream": False},
    timeout=120,
)
response.raise_for_status()
print(response.json()["message"]["content"])


# Currently, this is NOT using any tool. It might produce an incorrect result.