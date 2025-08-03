# ✨ TypoCorrectorUsingPython

`TypoCorrector` is a lightweight Python automation tool that uses a local LLM (via [Ollama](https://ollama.com/)) to correct **typos**, **casing**, and **punctuation** in real-time text. It runs in the background and allows quick fixes using simple hotkeys.

---

## 🔧 Features

- 🔤 Automatically corrects text with proper punctuation and casing
- ⚡ Hotkey-based:
  - `F9` – Fix currently selected text
  - `F10` – Fix the entire current line
- 🧠 Uses a locally running Ollama model (default: Mistral)
- 📋 Clipboard-safe and non-destructive
- 💻 Built with `pynput`, `pyperclip`, and `httpx`

---

## 📦 Requirements

Install the necessary dependencies:

```bash
pip install pynput pyperclip httpx
