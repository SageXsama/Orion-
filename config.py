"""
Orion assistant configuration.
Edit these values to match your setup.
"""

# --- Wake words ---
# Both phrases wake Orion. Uses openWakeWord — fully open source, no
# account or API key needed. Each .onnx model is trained for free via
# openWakeWord's Colab notebook (see README).
WAKE_WORDS = [
    {
        "name": "Wake up Orion",
        "path": "wake_words/wake_up_orion.onnx",
    },
    {
        "name": "Orion",
        "path": "wake_words/orion.onnx",
    },
]

# Confidence threshold (0-1) for triggering a wake word. Lower = more
# sensitive but more false triggers. Start at 0.5 and tune from there.
WAKE_WORD_THRESHOLD = 0.5

# --- Local LLM (Ollama) ---
OLLAMA_MODEL = "llama3.1:8b"
OLLAMA_URL = "http://localhost:11434/api/chat"

# System prompt that shapes Orion's personality and tells it how to
# request system actions.
SYSTEM_PROMPT = """You are Orion, a concise, helpful personal assistant \
running locally on the user's laptop. Keep spoken replies short and \
natural. If the user's request requires a system action (opening an \
app, changing volume, running a script), respond ONLY with a JSON \
object in this exact form and nothing else:
{"action": "<action_name>", "args": {...}}
Otherwise, just reply normally in plain text.
"""

# --- Speech ---
WHISPER_MODEL_SIZE = "small"  # tiny, base, small, medium — bigger = more accurate, slower
PIPER_VOICE_PATH = "voices/en_US-lessac-medium.onnx"  # download from Piper voices repo
RECORD_SECONDS = 5  # how long to listen after wake word before transcribing
SAMPLE_RATE = 16000

