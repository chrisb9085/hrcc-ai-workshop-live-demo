"""
LIVE BUILD: An AI Agent From Scratch -- SOLUTION
Stack: Ollama (local LLM) + api.frankfurter.dev
Loop:  PERCEIVE -> REASON -> DECIDE -> ACT -> REFLECT -> (back to PERCEIVE)
Setup: ollama serve   /   ollama pull qwen2.5:3b-instruct
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
        # 2. REASON -- model looks at everything so far and thinks about what to do.
        print("[REASON] thinking...")
        reply = call_model(messages)
        messages.append(reply)

        # 3. DECIDE -- does it want to use a tool, or is it ready to answer?
        tool_call = reply.get("tool_calls", [None])[0]

        if tool_call is None:
            print("[DECIDE] no tool needed -- final answer ready.")
            return reply["content"]

        print(f"[DECIDE] wants to call: {tool_call['function']['name']}")

        # 4. ACT -- WE run the real function. The model can only request it.
        args = tool_call["function"]["arguments"]
        result = get_exchange_rate(**args)
        print(f"[ACT] ran get_exchange_rate({args}) -> {result}")

        # 5. REFLECT -- feed the result back in. Model sees it on the next loop.
        messages.append({"role": "tool", "content": json.dumps(result)})
        # back to step 1: PERCEIVE


if __name__ == "__main__":
    answer = run_agent("What is 250 US dollars in Euros right now?")
    print(f"\nFINAL ANSWER: {answer}")