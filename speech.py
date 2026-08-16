"""
Handles voice I/O:
  - record_and_transcribe(): records mic audio after the wake word and
    returns the transcribed text (faster-whisper, fully offline)
  - speak(text): speaks a reply out loud (Piper TTS, fully offline)
"""

import io
import wave

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel
from piper.voice import PiperVoice

import config

print("[Orion] Loading speech models (first run may take a moment)...")
_whisper_model = WhisperModel(config.WHISPER_MODEL_SIZE, compute_type="int8")
_piper_voice = PiperVoice.load(config.PIPER_VOICE_PATH)
print("[Orion] Speech models ready.")


def record_and_transcribe() -> str:
    print(f"[Orion] Listening for {config.RECORD_SECONDS}s...")
    audio = sd.rec(
        int(config.RECORD_SECONDS * config.SAMPLE_RATE),
        samplerate=config.SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()

    segments, _ = _whisper_model.transcribe(
        audio.flatten().astype(np.float32) / 32768.0,
        language="en",
    )
    text = " ".join(segment.text.strip() for segment in segments).strip()
    print(f"[Orion] Heard: {text!r}")
    return text


def speak(text: str) -> None:
    print(f"[Orion] Saying: {text!r}")

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        _piper_voice.synthesize(text, wav_file)

    buffer.seek(0)
    with wave.open(buffer, "rb") as wav_file:
        rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    sd.play(audio, samplerate=rate)
    sd.wait()
