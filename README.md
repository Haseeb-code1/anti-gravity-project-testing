# Anti-Gravity Secure Projects Collection

This repository contains a collection of secure desktop applications built with Python and Tkinter, focusing on strong cryptographic principles and modern, user-friendly interfaces.

## 1. Secure Desktop Password Generator

A robust and highly customizable password generator that ensures cryptographically secure password generation using Python's `secrets` module. It features a modern dark/light mode UI and evaluates password strength based on entropy.

### Features
- **Cryptographically Secure:** Uses the `secrets` module for reliable randomness.
- **Customizable Constraints:** Toggle uppercase, lowercase, digits, and special characters.
- **Ambiguous Character Exclusion:** Option to remove easily confused characters (e.g., `l, I, 1, O, 0`).
- **Entropy & Strength Evaluation:** Calculates mathematical entropy and visually indicates password strength (Weak, Medium, Strong).
- **Clipboard Integration:** Easily copy the generated password with a single click.
- **History Tracking:** Safely saves a local history of generated passwords to a JSON file.
- **Modern UI:** Built with Tkinter, featuring a sleek design with built-in Dark and Light themes.

### Usage
Run the application using:
```bash
python main.py
```

### Testing
Run the comprehensive unit test suite:
```bash
python -m unittest test_generator.py
```

