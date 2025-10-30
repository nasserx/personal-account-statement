import tkinter as tk
from tkinter import Frame, Label, Entry, Button, messagebox
from utils.validation import validate_passcode

class PasscodeDialog:
    def __init__(self, parent, title, message):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x200")
        self.top.resizable(False, False)
        self.top.configure(bg='#f0f0f0')
        self.top.transient(parent)
        self.top.grab_set()
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        
        self.result = None
        
        # Center the window
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.top.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.top.winfo_height()) // 2
        self.top.geometry(f"+{x}+{y}")
        
        # Create UI elements
        form_frame = Frame(self.top, bg='#f0f0f0', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label
        message_label = Label(form_frame, text=message, font=("Arial", 12, "bold"), 
                             bg='#f0f0f0', wraplength=350)
        message_label.pack(pady=(0, 20))
        
        # passcode entry
        passcode_frame = Frame(form_frame, bg='#f0f0f0')
        passcode_frame.pack(fill=tk.X, pady=10)
        
        self.passcode_entry = Entry(passcode_frame, font=("Arial", 14, "bold"), width=20, 
                                  justify="center", show="*")
        self.passcode_entry.pack(pady=5)
        
        # Validation label
        self.validation_label = Label(passcode_frame, text="", font=("Arial", 10), 
                                     bg='#f0f0f0', fg='red')
        self.validation_label.pack()
        
        # Buttons
        button_frame = Frame(form_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        Button(button_frame, text="OK", command=self.validate_passcode, 
              font=("Arial", 12, "bold"), bg="#3f6fde", fg="white", 
              width=10).pack(side=tk.LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=self.cancel, 
              font=("Arial", 12, "bold"), bg="#3f6fde", fg="white", 
              width=10).pack(side=tk.LEFT, padx=10)
        
        # Bind Enter key
        self.passcode_entry.bind("<Return>", lambda e: self.validate_passcode())
        
        # Focus on passcode entry
        self.top.after(100, lambda: self.passcode_entry.focus_force())

    def validate_passcode(self):
        passcode = self.passcode_entry.get().strip()
        
        if not validate_passcode(passcode):
            messagebox.showerror("", "Passcode must be exactly 4 digits.")
            return 
        
        self.result = passcode
        self.top.destroy()
    
    def cancel(self):
        self.top.destroy()
