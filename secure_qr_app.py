import tkinter as tk
from tkinter import messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

class SecureQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure QR - Antigravity Edition")
        self.root.geometry("500x550")
        self.root.configure(bg="#2b2b2b")
        
        # --- Security: Load or Generate Encryption Key ---
        self.key_file = "secret.key"
        self.key = self.load_or_generate_key()
        
        # --- App State ---
        self.qr_image = None
        self.qr_photo = None
        
        # --- Antigravity Animation Variables ---
        self.y_offset = 0.0
        self.direction = 1
        
        self.setup_ui()
        self.animate_antigravity()
        
    def load_or_generate_key(self):
        """Loads the encryption key from a file, or generates one if it doesn't exist."""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = get_random_bytes(16)  # AES-128 key
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def encrypt_data(self, data: str) -> bytes:
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        # Combine nonce, tag, and ciphertext for easy storage
        return base64.b64encode(cipher.nonce + tag + ciphertext)

    def decrypt_data(self, encrypted_data: bytes) -> str:
        raw_data = base64.b64decode(encrypted_data)
        nonce = raw_data[:16]
        tag = raw_data[16:32]
        ciphertext = raw_data[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

    def setup_ui(self):
        """Sets up the Tkinter GUI layout."""
        # Title
        title_label = tk.Label(self.root, text="Secure QR Generator & Reader", 
                               font=("Helvetica", 16, "bold"), bg="#2b2b2b", fg="#00ffcc")
        title_label.pack(pady=15)
        
        # Input Section
        input_frame = tk.Frame(self.root, bg="#2b2b2b")
        input_frame.pack(pady=5)
        
        tk.Label(input_frame, text="Secret Data:", bg="#2b2b2b", fg="white").pack(side=tk.LEFT, padx=5)
        self.data_entry = tk.Entry(input_frame, width=35, font=("Helvetica", 10))
        self.data_entry.pack(side=tk.LEFT, padx=5)
        
        # Buttons Section
        btn_frame = tk.Frame(self.root, bg="#2b2b2b")
        btn_frame.pack(pady=15)
        
        btn_style = {"bg": "#444444", "fg": "white", "activebackground": "#666666", 
                     "font": ("Helvetica", 10, "bold"), "relief": tk.FLAT, "padx": 10, "pady": 5}
        tk.Button(btn_frame, text="Generate QR", command=self.generate_qr, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Save QR", command=self.save_qr, **btn_style).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Upload & Read", command=self.read_qr, **btn_style).pack(side=tk.LEFT, padx=10)
        
        # Antigravity Canvas (QR Display)
        self.canvas = tk.Canvas(self.root, width=260, height=260, bg="#1a1a1a", 
                                highlightthickness=2, highlightbackground="#00ffcc")
        self.canvas.pack(pady=15)
        
        # Placeholder floating text
        self.canvas.create_text(130, 130, text="Ready for Data...", fill="#00ffcc", 
                                font=("Helvetica", 12, "italic"), tags="floating")
        
        # Results Section
        tk.Label(self.root, text="Decrypted Result / Status:", bg="#2b2b2b", fg="white", font=("Helvetica", 10, "bold")).pack(pady=(5, 0))
        self.result_text = tk.Text(self.root, height=3, width=50, bg="#1a1a1a", fg="#00ffcc", font=("Courier", 10), state=tk.DISABLED, relief=tk.FLAT)
        self.result_text.pack(pady=5)

    def animate_antigravity(self):
        """Simulates a zero-gravity floating effect on elements with the 'floating' tag."""
        if self.y_offset > 8:
            self.direction = -1
        elif self.y_offset < -8:
            self.direction = 1
            
        move_y = self.direction * 0.3
        self.y_offset += move_y
        
        self.canvas.move("floating", 0, move_y)
        self.root.after(33, self.animate_antigravity)

    def generate_qr(self):
        """Encrypts the input data and generates a QR code."""
        data = self.data_entry.get()
        if not data:
            messagebox.showwarning("Input Error", "Please enter data to encrypt and generate QR.")
            return
            
        try:
            encrypted_data = self.encrypt_data(data)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))
            return
            
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=2,
        )
        qr.add_data(encrypted_data)
        qr.make(fit=True)
        
        self.qr_image = qr.make_image(fill_color="#00ffcc", back_color="#1a1a1a").convert('RGB')
        self.qr_image = self.qr_image.resize((220, 220), Image.Resampling.LANCZOS)
        self.qr_photo = ImageTk.PhotoImage(self.qr_image)
        
        self.canvas.delete("all")
        self.canvas.create_image(130, 130 + self.y_offset, image=self.qr_photo, tags="floating")
        self.show_result("QR Code generated successfully. Data is safely encrypted.")

    def save_qr(self):
        """Saves the currently displayed QR code to a file."""
        if not self.qr_image:
            messagebox.showwarning("Save Error", "No QR code to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if file_path:
            self.qr_image.save(file_path)
            self.show_result(f"QR Code saved to: {file_path}")

    def read_qr(self):
        """Uploads an image, decodes the QR, and decrypts the data."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp"), ("All Files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            image = Image.open(file_path).convert('RGB')
            self.qr_image = image.resize((220, 220), Image.Resampling.LANCZOS)
            self.qr_photo = ImageTk.PhotoImage(self.qr_image)
            
            self.canvas.delete("all")
            self.canvas.create_image(130, 130 + self.y_offset, image=self.qr_photo, tags="floating")
            # Decode QR using OpenCV
            cv_img = cv2.imread(file_path)
            detector = cv2.QRCodeDetector()
            data, bbox, _ = detector.detectAndDecode(cv_img)
            
            if not data:
                messagebox.showerror("Read Error", "No QR code found in the image.")
                self.show_result("Scan failed.")
                return
                
            # OpenCV returns strings, but our data is base64 encoded bytes
            encrypted_data = data.encode('utf-8')
            decrypted_data = self.decrypt_data(encrypted_data)
            self.show_result(decrypted_data)
            
        except Exception as e:
            messagebox.showerror("Decryption/Read Error", f"Failed to process QR code.\nEnsure this image was generated with the current secret.key.\n\nDetails: {str(e)}")

    def show_result(self, text):
        """Displays text in the read-only result text box."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureQRApp(root)
    root.mainloop()
