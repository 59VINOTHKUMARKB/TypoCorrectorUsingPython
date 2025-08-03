from pynput import keyboard
from pynput.keyboard import Key, Controller
import pyperclip
import time
import httpx
from string import Template

controller = Controller()

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters:
$text
Return only the corrected text, don't include a preamble."""
)

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
OLLAMA_CONFIG = {
    "model": "mistral:7b-instruct-v0.2-q4_K_S",
    "keep_alive": "5m",
    "stream": False
}

def fix_text(text: str):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    try:
        response = httpx.post(
            OLLAMA_ENDPOINT,
            json={**OLLAMA_CONFIG, "prompt": prompt},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
    except Exception as e:
        print(f"[ERROR] Could not contact Ollama: {e}")
        return text

    if response.status_code != 200:
        print(f"[ERROR] Ollama returned status {response.status_code}: {response.text}")
        return text

    try:
        result = response.json().get("response", "").strip()
        return result if result else text
    except Exception as e:
        print(f"[ERROR] Failed to parse Ollama response: {e}")
        return text

def fix_current_line():
    controller.press(Key.home)
    controller.release(Key.home)
    time.sleep(0.05)

    controller.press(Key.shift)
    controller.press(Key.end)
    controller.release(Key.end)
    controller.release(Key.shift)
    time.sleep(0.05)

    fix_selection()

def fix_selection():
    with controller.pressed(Key.ctrl):
        controller.press('c')
        controller.release('c')

    time.sleep(0.2)
    text = pyperclip.paste()
    print(f"[DEBUG] Selected text: {text}")

    fixed_text = fix_text(text)
    print(f"[DEBUG] Fixed text: {fixed_text}")

    pyperclip.copy(fixed_text)
    time.sleep(0.01)

    with controller.pressed(Key.ctrl):
        controller.press('v')
        controller.release('v')

def on_f9():
    print("[INFO] F9 pressed - Fix selection")
    fix_selection()

def on_f10():
    print("[INFO] F10 pressed - Fix current line")
    fix_current_line()

with keyboard.GlobalHotKeys({
    '<f9>': on_f9,
    '<f10>': on_f10
}) as h:
    print("[INFO] Hotkeys ready: F9 (fix selection), F10 (fix current line)")
    h.join()
