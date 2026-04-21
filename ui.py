import tkinter as tk
from tkinter import ttk, messagebox
from generator import generate_password, calculate_entropy, evaluate_strength
from utils import DARK_THEME, LIGHT_THEME, copy_to_clipboard, save_password_to_file

class PasswordGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Secure Password Generator")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.is_dark_mode = True
        self.theme = DARK_THEME
        
        # State variables
        self.length_var = tk.IntVar(value=16)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        self.save_to_file = tk.BooleanVar(value=False)
        self.show_password = tk.BooleanVar(value=True)
        self.generated_password = ""
        
        self.setup_ui()
        self.apply_theme()
        
        # Keyboard shortcut: Enter to generate
        self.root.bind("<Return>", lambda event: self.generate_btn_clicked())
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(self.header_frame, text="Password Generator", font=("Helvetica", 18, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        self.theme_btn = tk.Button(self.header_frame, text="Toggle Theme", command=self.toggle_theme, cursor="hand2", relief=tk.FLAT)
        self.theme_btn.pack(side=tk.RIGHT)
        
        # Length Slider
        self.length_frame = tk.Frame(self.main_frame)
        self.length_frame.pack(fill=tk.X, pady=10)
        
        self.length_label = tk.Label(self.length_frame, text="Password Length: 16", font=("Helvetica", 12))
        self.length_label.pack(anchor=tk.W)
        
        self.length_slider = ttk.Scale(self.length_frame, from_=6, to_=64, orient=tk.HORIZONTAL, variable=self.length_var, command=self.update_length_label)
        self.length_slider.pack(fill=tk.X, pady=5)
        
        # Options Frame
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(fill=tk.X, pady=15, ipady=10, ipadx=10)
        
        self.upper_cb = tk.Checkbutton(self.options_frame, text="Uppercase Letters (A-Z)", variable=self.use_upper, font=("Helvetica", 10))
        self.upper_cb.pack(anchor=tk.W, pady=2)
        
        self.lower_cb = tk.Checkbutton(self.options_frame, text="Lowercase Letters (a-z)", variable=self.use_lower, font=("Helvetica", 10))
        self.lower_cb.pack(anchor=tk.W, pady=2)
        
        self.digits_cb = tk.Checkbutton(self.options_frame, text="Numbers (0-9)", variable=self.use_digits, font=("Helvetica", 10))
        self.digits_cb.pack(anchor=tk.W, pady=2)
        
        self.special_cb = tk.Checkbutton(self.options_frame, text="Special Characters (!@#$)", variable=self.use_special, font=("Helvetica", 10))
        self.special_cb.pack(anchor=tk.W, pady=2)
        
        self.ambiguous_cb = tk.Checkbutton(self.options_frame, text="Exclude Ambiguous (l, I, 1, O, 0)", variable=self.exclude_ambiguous, font=("Helvetica", 10))
        self.ambiguous_cb.pack(anchor=tk.W, pady=2)
        
        self.save_cb = tk.Checkbutton(self.options_frame, text="Save generated password to file", variable=self.save_to_file, font=("Helvetica", 10))
        self.save_cb.pack(anchor=tk.W, pady=2)
        
        # Generate Button
        self.generate_btn = tk.Button(self.main_frame, text="GENERATE PASSWORD", font=("Helvetica", 12, "bold"), command=self.generate_btn_clicked, cursor="hand2", relief=tk.FLAT, pady=10)
        self.generate_btn.pack(fill=tk.X, pady=20)
        
        # Output Area
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.X, pady=5)
        
        self.output_entry = tk.Entry(self.output_frame, font=("Courier", 16), justify=tk.CENTER, state="readonly", relief=tk.FLAT)
        self.output_entry.pack(fill=tk.X, ipady=12)
        
        # Controls Frame
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        self.copy_btn = tk.Button(self.controls_frame, text="Copy to Clipboard", command=self.copy_password, cursor="hand2", relief=tk.FLAT, pady=5)
        self.copy_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))
        
        self.show_cb = tk.Checkbutton(self.controls_frame, text="Show Password", variable=self.show_password, command=self.toggle_show_password, font=("Helvetica", 10))
        self.show_cb.pack(side=tk.RIGHT)
        
        # Status/Strength Frame
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=15, ipady=10, ipadx=10)
        
        self.strength_label = tk.Label(self.status_frame, text="Strength: -", font=("Helvetica", 12, "bold"))
        self.strength_label.pack(side=tk.LEFT)
        
        self.entropy_label = tk.Label(self.status_frame, text="Entropy: - bits", font=("Helvetica", 10))
        self.entropy_label.pack(side=tk.RIGHT)

    def update_length_label(self, event=None):
        """Updates the length label when slider moves."""
        self.length_label.config(text=f"Password Length: {self.length_var.get()}")

    def generate_btn_clicked(self):
        """Generates the password and updates UI."""
        try:
            pwd = generate_password(
                length=self.length_var.get(),
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_special=self.use_special.get(),
                exclude_ambiguous=self.exclude_ambiguous.get()
            )
            self.generated_password = pwd
            self.update_output_display()
            
            # Entropy & Strength Calculations
            entropy = calculate_entropy(pwd)
            strength = evaluate_strength(entropy)
            
            self.entropy_label.config(text=f"Entropy: {entropy:.1f} bits")
            self.strength_label.config(text=f"Strength: {strength}")
            
            # Color code strength
            if strength == "Weak":
                self.strength_label.config(fg=self.theme["error"])
            elif strength == "Medium":
                self.strength_label.config(fg=self.theme["warning"])
            else:
                self.strength_label.config(fg=self.theme["success"])
                
            if self.save_to_file.get():
                save_password_to_file(pwd)
                
        except ValueError as e:
            messagebox.showwarning("Selection Error", str(e))

    def update_output_display(self):
        """Updates the output entry based on show/hide toggle."""
        self.output_entry.config(state="normal")
        self.output_entry.delete(0, tk.END)
        if self.show_password.get():
            self.output_entry.insert(0, self.generated_password)
            self.output_entry.config(show="")
        else:
            self.output_entry.insert(0, self.generated_password)
            self.output_entry.config(show="*")
        self.output_entry.config(state="readonly")

    def toggle_show_password(self):
        """Triggered by Show Password checkbox."""
        self.update_output_display()

    def copy_password(self):
        """Copies the password and shows success."""
        if self.generated_password:
            copy_to_clipboard(self.root, self.generated_password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "Generate a password first!")

    def toggle_theme(self):
        """Toggles between Light and Dark mode."""
        self.is_dark_mode = not self.is_dark_mode
        self.theme = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        self.apply_theme()

    def apply_theme(self):
        """Applies colors to all widgets based on active theme."""
        bg = self.theme["bg"]
        fg = self.theme["fg"]
        frame_bg = self.theme["frame_bg"]
        btn_bg = self.theme["button_bg"]
        btn_fg = self.theme["button_fg"]
        entry_bg = self.theme["entry_bg"]
        entry_fg = self.theme["entry_fg"]
        
        self.root.configure(bg=bg)
        self.main_frame.configure(bg=bg)
        self.header_frame.configure(bg=bg)
        self.length_frame.configure(bg=bg)
        self.options_frame.configure(bg=frame_bg)
        self.output_frame.configure(bg=bg)
        self.controls_frame.configure(bg=bg)
        self.status_frame.configure(bg=frame_bg)
        
        self.title_label.configure(bg=bg, fg=self.theme["accent"])
        self.theme_btn.configure(bg=btn_bg, fg=btn_fg, activebackground=self.theme["button_active"])
        self.length_label.configure(bg=bg, fg=fg)
        
        # Checkbuttons styling
        cb_opts = {"bg": frame_bg, "fg": fg, "selectcolor": frame_bg, "activebackground": frame_bg, "activeforeground": fg}
        self.upper_cb.configure(**cb_opts)
        self.lower_cb.configure(**cb_opts)
        self.digits_cb.configure(**cb_opts)
        self.special_cb.configure(**cb_opts)
        self.ambiguous_cb.configure(**cb_opts)
        self.save_cb.configure(**cb_opts)
        
        self.show_cb.configure(bg=bg, fg=fg, selectcolor=bg, activebackground=bg, activeforeground=fg)
        self.generate_btn.configure(bg=self.theme["accent"], fg=bg, activebackground=self.theme["success"])
        self.output_entry.configure(bg=entry_bg, fg=entry_fg, readonlybackground=entry_bg)
        self.copy_btn.configure(bg=btn_bg, fg=btn_fg, activebackground=self.theme["button_active"])
        
        # Retain color code if password exists
        if not self.generated_password:
            self.strength_label.configure(bg=frame_bg, fg=fg)
        else:
            self.strength_label.configure(bg=frame_bg)
            
        self.entropy_label.configure(bg=frame_bg, fg=fg)
