import tkinter as tk
from tkinter import Frame, Label, Entry, Button, messagebox
from utils.validation import validate_required_fields, validate_amount

class EnhancedTransactionDialog:
    def __init__(self, parent, transaction_type):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Add New {transaction_type}")
        self.top.geometry("400x330")
        self.top.resizable(False, False)
        self.top.configure(bg='#f0f0f0')
        self.top.transient(parent)
        self.top.grab_set()
        
        self.result = None
        self.transaction_type = transaction_type
        
        # Center the window
        self.top.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.top.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.top.winfo_height()) // 2
        self.top.geometry(f"+{x}+{y}")
        
        # Create UI elements
        form_frame = Frame(self.top, bg='#f0f0f0', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Amount field
        amount_frame = Frame(form_frame, bg='#f0f0f0')
        amount_frame.pack(fill=tk.X, pady=10)
        
        Label(amount_frame, text="Amount:", font=("Arial", 12), 
              bg='#f0f0f0').pack(padx=5)
        
        self.amount_entry = Entry(amount_frame, font=("Arial", 12), width=30, justify="center")
        self.amount_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # From/To field based on transaction type
        if transaction_type == "Deposit":
            # For Deposit: "From" field only (source)
            from_frame = Frame(form_frame, bg='#f0f0f0')
            from_frame.pack(fill=tk.X, pady=10)
            
            Label(from_frame, text="From:", font=("Arial", 12), 
                  bg='#f0f0f0').pack(padx=5)
            
            self.from_entry = Entry(from_frame, font=("Arial", 12), width=30, justify="center")
            self.from_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # "To" field is empty for deposit
            self.to_entry = None
        else:
            # For Withdrawal: "To" field only (recipient)
            to_frame = Frame(form_frame, bg='#f0f0f0')
            to_frame.pack(fill=tk.X, pady=10)
            
            Label(to_frame, text="To:", font=("Arial", 12), 
                  bg='#f0f0f0').pack(padx=5)
            
            self.to_entry = Entry(to_frame, font=("Arial", 12), width=30, justify="center")
            self.to_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # "From" field is empty for withdrawal
            self.from_entry = None
        
        # Description field
        desc_frame = Frame(form_frame, bg='#f0f0f0')
        desc_frame.pack(fill=tk.X, pady=10)
        
        Label(desc_frame, text="Description:", font=("Arial", 12), 
              bg='#f0f0f0').pack(padx=5)
        
        self.desc_entry = Entry(desc_frame, font=("Arial", 12), width=30, justify="center")
        self.desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Buttons
        button_frame = Frame(form_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        Button(button_frame, text="Add", command=self.ok, font=("Arial", 12, "bold"), 
              bg="#3f6fde", fg="white", width=10).pack(side=tk.LEFT, padx=10)
        
        Button(button_frame, text="Cancel", command=self.cancel, font=("Arial", 12, "bold"), 
              bg="#3f6fde", fg="white", width=10).pack(side=tk.LEFT, padx=10)
        
        # Make Enter key move between fields and submit
        self.amount_entry.bind("<Return>", lambda e: self.next_field(self.amount_entry))
        
        if self.from_entry:
            self.from_entry.bind("<Return>", lambda e: self.next_field(self.from_entry))
        
        if self.to_entry:
            self.to_entry.bind("<Return>", lambda e: self.next_field(self.to_entry))
            
        self.desc_entry.bind("<Return>", lambda e: self.ok())
        
        # Focus on first input field
        self.amount_entry.focus()
    
    def next_field(self, current_field):
        """Move to next field"""
        if current_field == self.amount_entry:
            if self.from_entry:
                self.from_entry.focus()
            elif self.to_entry:
                self.to_entry.focus()
            else:
                self.desc_entry.focus()
        elif current_field == self.from_entry:
            self.desc_entry.focus()
        elif current_field == self.to_entry:
            self.desc_entry.focus()
    
    def ok(self):
        amount = self.amount_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if self.transaction_type == "Deposit":
            from_account = self.from_entry.get().strip() if self.from_entry else ""
            to_account = ""
            if not validate_required_fields(amount, from_account, description):
                messagebox.showerror("Error", "Please fill all fields")
                return
        else:
            from_account = ""
            to_account = self.to_entry.get().strip() if self.to_entry else ""
            if not validate_required_fields(amount, to_account, description):
                messagebox.showerror("Error", "Please fill all fields")
                return
        
        # Validate amount
        is_valid, amount_value = validate_amount(amount)
        if not is_valid:
            messagebox.showerror("Error", "Amount must be a positive number")
            return
        
        self.result = (amount, from_account, to_account, description)
        self.top.destroy()
    
    def cancel(self):
        self.top.destroy()