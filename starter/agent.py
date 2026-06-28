"""
LIVE BUILD: An AI Agent From Scratch -- STARTER
Stack: Ollama (local LLM) + api.frankfurter.dev (free, no-key currency API)
Loop:  PERCEIVE -> REASON -> DECIDE -> ACT -> REFLECT -> (back to PERCEIVE)
Setup: ollama serve   /   ollama pull qwen2.5:3b-instruct

Everything above run_agent() is already built for you. We write run_agent() live.
"""
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b-instruct"
CONTEXT_WINDOW = 32768  # tool-calling gets unreliable below ~32k context


def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """The TOOL. The model can only ASK us to run this -- it never runs it itself."""
    url = "https://api.frankfurter.dev/v1/latest"
    params = {"base": from_currency.upper(), "symbols": to_currency.upper()}
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    return r.json()


# The SCHEMA: tells the model this tool exists and how to use it.
TOOLS = [{
    "type": "function",
    "function": {
        "name": "get_exchange_rate",
        "description": "Get the current real-world exchange rate between two currencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_currency": {"type": "string", "description": "3-letter code FROM, e.g. USD"},
                "to_currency": {"type": "string", "description": "3-letter code TO, e.g. EUR"},
            },
            "required": ["from_currency", "to_currency"],
        },
    },
}]


def call_model(messages):
    """Sends our conversation so far to the local model and gets its reply."""
    payload = {"model": MODEL, "messages": messages, "tools": TOOLS,
               "stream": False, "options": {"num_ctx": CONTEXT_WINDOW}}
    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["message"]


def run_agent(question: str):
    # 1. PERCEIVE -- the conversation list IS the agent's memory of what's happened.
    messages = [{"role": "user", "content": question}]
    print(f"\n[PERCEIVE] {question}")

    while True:
        # TODO 2. REASON -- call call_model(messages) to get the model's reply,
        # then append that reply onto `messages` (so it remembers what it said).
        

        # TODO 3. DECIDE -- check reply.get("tool_calls", [None])[0].
        # If it's None: the model is done. print [DECIDE] and return reply["content"].
        # If it's NOT None: print which tool it wants to call, and keep going.

        # TODO 4. ACT -- pull `args = tool_call["function"]["arguments"]`,
        # then call get_exchange_rate(**args) to get a real result. Print it.

        # TODO 5. REFLECT -- append the result back onto `messages` as
        # {"role": "tool", "content": json.dumps(result)} so the model
        # "perceives" it the next time through this loop.

        break  # <-- delete this line once your loop above actually loops


if __name__ == "__main__":
    answer = run_agent("What is 250 US dollars in Euros right now?")
    print(f"\nFINAL ANSWER: {answer}")