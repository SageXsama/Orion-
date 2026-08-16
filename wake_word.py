"""
Listens continuously for any of Orion's wake phrases (see config.WAKE_WORDS)
using openWakeWord — fully open source, no account or API key required.
When one is detected above config.WAKE_WORD_THRESHOLD, calls on_wake().
"""

import numpy as np
import pyaudio
from openwakeword.model import Model

import config

CHUNK_SAMPLES = 1280  # openWakeWord expects 80ms chunks at 16kHz


def listen_for_wake_word(on_wake):
    model_paths = [w["path"] for w in config.WAKE_WORDS]
    oww_model = Model(wakeword_models=model_paths, inference_framework="onnx")

    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=CHUNK_SAMPLES,
    )

    names = ", ".join(repr(w["name"]) for w in config.WAKE_WORDS)
    print(f"[Orion] Listening for: {names}...")

    try:
        while True:
            audio_chunk = np.frombuffer(
                stream.read(CHUNK_SAMPLES, exception_on_overflow=False),
                dtype=np.int16,
            )
            predictions = oww_model.predict(audio_chunk)

            for model_name, score in predictions.items():
                if score > config.WAKE_WORD_THRESHOLD:
                    print(f"[Orion] Wake word detected: '{model_name}' ({score:.2f})")
                    oww_model.reset()  # clear buffers so it doesn't retrigger instantly
                    on_wake()
                    break

    except KeyboardInterrupt:
        print("\n[Orion] Stopping wake word listener.")

    finally:
        stream.close()
        pa.terminate()
