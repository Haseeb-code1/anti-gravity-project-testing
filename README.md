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

---

## 2. Secure QR Code Generator & Reader

A secure application to encrypt sensitive data and encode it into a QR code, as well as read and decrypt data from an existing QR code image.

### Features
- **AES-GCM Encryption:** Data is securely encrypted using AES in GCM mode before being stored in the QR code.
- **Automated Key Management:** Automatically generates or loads a `secret.key` file for encryption/decryption.
- **QR Code Generation:** Converts encrypted data into a visually distinct QR code.
- **QR Code Reading:** Uses OpenCV to scan and decode QR codes from uploaded images.
- **Antigravity UI Effect:** Features a dynamic Tkinter interface with "floating" UI elements.

### Usage
Run the application using:
```bash
python secure_qr_app.py
```

### Testing
Run the unit test suite:
```bash
python -m unittest test_secure_qr_app.py
```

## Requirements
Ensure you have the required dependencies installed:
- `qrcode`
- `Pillow`
- `opencv-python`
- `pycryptodome`
- `numpy`

```bash
pip install qrcode Pillow opencv-python pycryptodome numpy
```
