"""
Executes system actions requested by the LLM, on Windows.
Add new actions here as your assistant grows.
"""

import os
import subprocess

# Map friendly app names to their Windows executable / start command.
# Add your own commonly used apps here.
APP_COMMANDS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "vscode": "code",
    "browser": "start chrome",
    "explorer": "explorer.exe",
}


def run_action(action: dict) -> str:
    name = action.get("action")
    args = action.get("args", {})

    if name == "open_app":
        app = args.get("name", "").lower()
        command = APP_COMMANDS.get(app)
        if not command:
            return f"I don't know how to open '{app}' yet."
        subprocess.Popen(command, shell=True)
        return f"Opening {app}."

    if name == "set_volume":
        # Requires nircmd.exe on PATH for simple volume control on Windows.
        # Download: https://www.nirsoft.net/utils/nircmd.html
        level = args.get("level", 50)  # 0-100
        scaled = int(level / 100 * 65535)
        subprocess.run(["nircmd", "setsysvolume", str(scaled)])
        return f"Volume set to {level}%."

    if name == "run_script":
        path = args.get("path")
        if not path or not os.path.exists(path):
            return "I couldn't find that script."
        subprocess.Popen(["python", path], shell=True)
        return f"Running {path}."

    return f"I don't know how to handle the action '{name}'."
