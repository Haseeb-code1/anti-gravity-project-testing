import json
import os
import tkinter as tk

# ──────────────────────────────────────────────
# Color Palettes
# ──────────────────────────────────────────────

DARK_THEME = {
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "accent": "#89b4fa",
    "entry_bg": "#313244",
    "entry_fg": "#cdd6f4",
    "button_bg": "#45475a",
    "button_fg": "#cdd6f4",
    "button_active": "#585b70",
    "frame_bg": "#181825",
    "success": "#a6e3a1",
    "warning": "#fab387",
    "error": "#f38ba8",
}

LIGHT_THEME = {
    "bg": "#eff1f5",
    "fg": "#4c4f69",
    "accent": "#1e66f5",
    "entry_bg": "#e6e9ef",
    "entry_fg": "#4c4f69",
    "button_bg": "#ccd0da",
    "button_fg": "#4c4f69",
    "button_active": "#bcc0cc",
    "frame_bg": "#dce0e8",
    "success": "#40a02b",
    "warning": "#df8e1d",
    "error": "#d20f39",
}

HISTORY_FILE = "passwords_history.json"

def copy_to_clipboard(root: tk.Tk, text: str):
    """Copies the given text to the system clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def save_password_to_file(password: str):
    """Saves a generated password to a local JSON file."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
            
    history.append({"password": password})
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"Failed to save password history: {e}")
