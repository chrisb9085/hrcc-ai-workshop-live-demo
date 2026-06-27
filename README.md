# Agentic AI Workshop -- Build Your Own Agent

We're building a tool-using AI agent **from scratch**, live, no frameworks --
just raw Python and a local LLM running on your own laptop.

## Setup Instructions

### 1. Install Python 3.10+
Check with `python3 --version` (or `python --version` on Windows). If you
don't have it: https://www.python.org/downloads/

### 2. Install Ollama (runs the LLM locally on your machine)
https://ollama.com/download -- pick your OS, install, then **restart your
terminal**.

### 3. Pull the model
```
ollama pull qwen2.5:3b-instruct
```
This is a few GB -- let it finish before you close your laptop.

### 4. Clone this repo and install Python dependencies
```
git clone <repo-url>
cd hrcc-ai-workshop-live-demo
pip install -r requirements.txt
```

### 5. Verify everything works
```
python step0.py
```
You should see the model respond (likely incorrectly/hedging -- that's
expected and is the whole point of this script). If you get a connection
error, Ollama isn't running -- see Troubleshooting below.

If you see a real response (right or wrong), **you're fully set up.** ✅

---

## What we're building

A four-letter-word's worth of concepts, in order, mapped straight to code:

```
PERCEIVE -> REASON -> DECIDE -> ACT -> REFLECT -> (loop back to PERCEIVE)
```

- `step0.py` -- already done, this is our "before" picture.
  A plain LLM call, no tools, asked something it can't know for certain.
- `starter/agent.py` -- what we build together, live. The boilerplate
  (the tool, its schema, the function that talks to Ollama) is already
  written; we write the `run_agent()` loop together, one stage at a time.
- `solution/agent.py` -- the finished version. If you fall behind or hit a
  bug you can't find, check here. No shame in peeking.


## Troubleshooting

**`ConnectionError` / `Connection refused` when running any script**
Ollama isn't running. Open a terminal and run `ollama serve`. If you get
`bind: address already in use`, Ollama is already running in the
background (normal on Windows/Mac) -- just leave it and try the script
again.

**First response is really slow**
Normal. The very first call also has to load the model into RAM. It gets
faster after that. Run it once before the workshop so this slow first call
doesn't happen live in front of everyone.

**`ModuleNotFoundError: No module named 'requests'`**
Run `pip install -r requirements.txt` again, and make sure you're using the
same `python3`/`pip` pairing (try `python3 -m pip install -r requirements.txt`
if unsure).

**I'm completely lost during the live build**
Open `solution/agent.py` side-by-side with `starter/agent.py` and diff them
line by line, or just swap to running the solution file so you can keep
following along conceptually without being stuck on a bug.