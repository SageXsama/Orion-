"""
Sends a prompt to the local Ollama model and returns either:
  - plain text (Orion's spoken reply), or
  - a dict like {"action": "...", "args": {...}} for system_control.py to run
"""

import json
import requests

import config

_history = [{"role": "system", "content": config.SYSTEM_PROMPT}]


def ask_orion(user_text: str):
    _history.append({"role": "user", "content": user_text})

    response = requests.post(
        config.OLLAMA_URL,
        json={
            "model": config.OLLAMA_MODEL,
            "messages": _history,
            "stream": False,
        },
        timeout=180,  # generous — first response after model load can be slow on CPU
    )
    response.raise_for_status()

    reply = response.json()["message"]["content"].strip()
    _history.append({"role": "assistant", "content": reply})

    # If the model responded with a JSON action, parse and return it
    if reply.startswith("{") and reply.endswith("}"):
        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            pass

    return reply


if __name__ == "__main__":
    # Quick manual test: python brain.py
    print("Type a message to Orion (Ctrl+C to quit).")
    while True:
        text = input("You: ")
        result = ask_orion(text)
        print("Orion:", result)
