# Orion — offline personal assistant

Wake words: **"Wake up Orion"** or just **"Orion"**
Platform: Windows

## What Orion does right now

Say a wake phrase → Orion listens for 5 seconds → transcribes what you
said → thinks about it → either speaks a reply or does something on your
laptop (opens an app, sets volume, runs a script).

Everything runs locally. Nothing is sent over the internet.

---

## Setup (do these in order)

Each step ends with a **✓ Check** — a way to confirm it actually worked
before you move to the next one.

### Step 1 — Install the Python packages
```
pip install -r requirements.txt
```
If `pyaudio` fails to install (common on Windows), run:
```
pip install pipwin
pipwin install pyaudio
```
then try `pip install -r requirements.txt` again.

**✓ Check:** run `python -c "import openwakeword, faster_whisper, piper"` —
no errors means everything installed.

### Step 2 — Install Ollama (the local AI brain)
1. Download and install from https://ollama.com
2. Open a terminal and run:
   ```
   ollama pull llama3.1:8b
   ```
   This downloads the model (a few GB — grab a coffee).
3. Leave Ollama running in the background. It automatically serves on
   `localhost:11434` — you don't need to start anything else.

**✓ Check:** run `python brain.py` in the `orion` folder, type "hello",
and press Enter. If Ollama replies, this step is done.

### Step 3 — Download openWakeWord's helper files
openWakeWord needs two small support models to work. Download them once:
```
python -c "import openwakeword; openwakeword.utils.download_models()"
```

**✓ Check:** the command finishes with no errors (it downloads a couple
small files, takes a few seconds).

### Step 4 — Create your two wake word files
This is the only slightly fiddly step. openWakeWord turns text into a
detector using a free notebook — no need to record your own voice.

1. Go to https://github.com/dscripka/openWakeWord
2. Open `notebooks/automatic_model_training.ipynb` in Google Colab (there's
   a button for this on the page)
3. Run the notebook once with the text `wake up orion` → it produces a
   `.onnx` file → download it, rename to `wake_up_orion.onnx`
4. Run the notebook a second time with the text `orion` → download →
   rename to `orion.onnx`
5. Put both files in a new folder: `orion/wake_words/`

**✓ Check:** you have `orion/wake_words/wake_up_orion.onnx` and
`orion/wake_words/orion.onnx` on disk.

> Heads up: "Orion" alone is a short, common-sounding word, so it may
> trigger by accident more than "Wake up Orion" does. If that happens,
> either delete it from `WAKE_WORDS` in `config.py`, or open `config.py`
> and raise `WAKE_WORD_THRESHOLD` from `0.5` toward `0.7`–`0.8` (higher =
> harder to trigger, fewer accidents).

### Step 5 — Download a voice for Orion to speak with
1. Go to https://github.com/rhasspy/piper/blob/master/VOICES.md
2. Pick any English voice marked "medium" quality (a good balance of
   speed and naturalness)
3. Download **two** files for that voice: the `.onnx` file and the
   `.onnx.json` file next to it
4. Put both in a new folder: `orion/voices/`
5. Open `config.py` and make sure `PIPER_VOICE_PATH` matches the exact
   filename you downloaded

**✓ Check:** `orion/voices/` contains both the `.onnx` and `.onnx.json`
files for your chosen voice.

### Step 6 — Run Orion
```
python main.py
```
You'll see `[Orion] Listening for...` in the terminal. Say "Wake up
Orion" or just "Orion" out loud, then speak your request. It'll listen
for 5 seconds, think, and reply out loud.

**✓ Check:** the terminal prints `[Orion] Wake word detected` when you
say the phrase, and you hear a spoken reply after you talk.

---

## If something's not working

Test each piece on its own instead of guessing:
- **No reply from Ollama?** → Step 2's check. Fix this first, nothing
  else works without it.
- **Wake word never triggers?** → confirm the two `.onnx` files exist in
  `orion/wake_words/` with the exact names in `config.py`.
- **No sound comes out?** → confirm both Piper files exist in
  `orion/voices/` and the path in `config.py` matches exactly.

## Customizing system actions

Open `system_control.py` and edit `APP_COMMANDS` to add apps you
actually use. To add a whole new kind of action (like "lock screen" or
"check battery"), add a new `if name == "...":` block there, and mention
the new action by name in the `SYSTEM_PROMPT` inside `config.py` so the
AI knows it's allowed to ask for it.

## What's next

1. **More system actions** — volume, brightness, file search, window
   management.
2. **Memory** — remember past conversations across restarts (currently
   it forgets everything when you close the program).
3. **Smarter listening** — right now Orion always records for a fixed
   5 seconds. A better version stops listening as soon as you stop
   talking, instead of waiting out the timer.
