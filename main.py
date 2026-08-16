"""
Orion — offline personal assistant.

Wake word -> listen -> transcribe -> think -> act or speak, all offline.
"""

import brain
import system_control
import speech
from wake_word import listen_for_wake_word


def handle_conversation():
    user_text = speech.record_and_transcribe()

    if not user_text:
        return  # heard nothing usable, go back to sleep

    if user_text.strip().lower() in ("sleep", "go to sleep", "stop listening"):
        speech.speak("Going back to sleep.")
        return

    result = brain.ask_orion(user_text)

    if isinstance(result, dict):
        outcome = system_control.run_action(result)
        speech.speak(outcome)
    else:
        speech.speak(result)


if __name__ == "__main__":
    listen_for_wake_word(on_wake=handle_conversation)
