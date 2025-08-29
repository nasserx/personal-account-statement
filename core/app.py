import tkinter as tk
from tkinter import ttk, messagebox, Frame, Label, Entry, Button
from datetime import datetime

from core.config import APP_TITLE, APP_ICON, ICONS_DIR
from utils.validation import validate_icon_path
from utils.file_utils import load_transactions, save_transactions, load_passcode, save_passcode
from dialogs.passcode_dialog import PasscodeDialog
from dialogs.transaction_dialog import EnhancedTransactionDialog
from dialogs.edit_dialog import EditTransactionDialog
import sys

class ModernTransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        
        if validate_icon_path(str(APP_ICON)):
            try:
                self.root.iconbitmap(str(APP_ICON))
            except:
                pass
        
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Make window full screen
        self.root.state('zoomed')
        
        # Application data
        self.transactions = []
        self.balance = 0.0
        
        # Check if first time running
        self.check_first_time()
        
        # Load previous data
        self.load_data()
        
        # Create user interface
        self.create_widgets()
        
        # Update display
        self.update_display()
    
    def check_first_time(self):
        """Check if this is the first time running the app"""
        if not load_passcode():
            self.setup_passcode()
        else:
            self.verify_passcode()
    
    def setup_passcode(self):
        """Setup passcode for first time users"""
        dialog = PasscodeDialog(self.root, "Setup Passcode", "Set a passcode:")
        self.root.wait_window(dialog.top)
        
        if dialog.result is None:
            # User cancelled, exit application
            sys.exit()
        
        if dialog.result:
            passcode = dialog.result
            # Save passcode to file
            save_passcode(passcode)
            messagebox.showinfo("Success", "passcode setup completed successfully!")

    def verify_passcode(self):
        """Verify passcode for returning users"""
        # Load saved passcode
        saved_passcode = load_passcode()
        
        # Show passcode dialog until correct passcode is entered
        while True:
            dialog = PasscodeDialog(self.root, "Enter passcode", "Enter your passcode:")
            self.root.wait_window(dialog.top)
            
            if dialog.result is None:
                # User cancelled, exit application
                sys.exit()
            
            if dialog.result == saved_passcode:
                return True
            else:
                messagebox.showerror("Error", "Incorrect passcode. Please try again.")
    
    def create_widgets(self):
        # Create main frame with modern design
        main_frame = Frame(self.root, bg='#f0f0f0', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Balance information panel
        balance_frame = Frame(main_frame, bg='white', relief=tk.RAISED, bd=0)
        balance_frame.pack(fill=tk.X, pady=(0, 20))
        
        balance_title = Label(balance_frame, text="Current Balance:", 
                             font=("Arial", 16, "bold"), bg='white')
        balance_title.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.balance_var = tk.StringVar()
        balance_value = Label(balance_frame, textvariable=self.balance_var, 
                             font=("Arial", 16, "bold"), bg='white')
        balance_value.pack(side=tk.LEFT, padx=15, pady=15)
        
        # Control buttons panel
        control_frame = Frame(main_frame, bg='#f0f0f0')
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Deposit and withdrawal buttons
        Button(control_frame, text="New Deposit", command=self.add_deposit, 
              bg='#27ae60', fg='white', font=("Arial", 12, "bold"), 
              width=15, height=1, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        
        Button(control_frame, text="New Withdrawal", command=self.add_withdrawal, 
              bg='#e74c3c', fg='white', font=("Arial", 12, "bold"), 
              width=15, height=1, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        
        # Edit Transaction button
        Button(control_frame, text="Edit Transaction", command=self.edit_transaction, 
              bg='#3498db', fg='white', font=("Arial", 12, "bold"), 
              width=15, height=1, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        
        # Delete Transaction button
        Button(control_frame, text="Delete Transaction", command=self.delete_transaction, 
              bg='#e67e22', fg='white', font=("Arial", 12, "bold"), 
              width=15, height=1, relief=tk.FLAT).pack(side=tk.LEFT, padx=10)
        
        # Quick search frame
        search_frame = Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        Label(search_frame, text="Quick search:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.quick_search)
        search_entry = Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=26)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind("<Return>", lambda e: self.quick_search())
        
        # Transactions filter
        Label(search_frame, text="Transaction filter:", font=("Arial", 12)).pack(side=tk.LEFT, padx=(20, 5))
        
        self.operation_var = tk.StringVar(value="All")
        operation_combo = ttk.Combobox(search_frame, textvariable=self.operation_var, 
                                      values=["All", "Deposit only", "Withdrawal only"], 
                                      state="readonly", width=15, font=("Arial", 12))
        operation_combo.pack(side=tk.LEFT, padx=5)
        operation_combo.bind("<<ComboboxSelected>>", self.filter_by_operation)
        
        # Search results frame
        self.search_results_frame = Frame(main_frame, relief=tk.RAISED, bd=0)
        self.search_results_frame.pack(fill=tk.X, pady=(0, 15))
        self.search_results_frame.pack_forget()
        
        self.search_results_var = tk.StringVar()
        search_results_label = Label(self.search_results_frame, textvariable=self.search_results_var, 
                                    font=("Arial", 11, "bold"))
        search_results_label.pack(pady=10)
        
        # Transactions table with bank-like design
        table_frame = Frame(main_frame, bg='white', relief=tk.SUNKEN, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Define columns in the requested order
        columns = ("date", "deposit", "from_account", "withdrawal", "to_account", "description", "balance")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 11, "bold"))

        
        # Define headings in the requested order
        self.tree.heading("date", text="Date")
        self.tree.heading("deposit", text="Deposit")
        self.tree.heading("from_account", text="From")
        self.tree.heading("withdrawal", text="Withdrawal")
        self.tree.heading("to_account", text="To")
        self.tree.heading("description", text="Description")
        self.tree.heading("balance", text="Balance")
        
        # Define columns with equal widths for deposit and withdrawal
        self.tree.column("date", width=150, anchor=tk.CENTER)
        self.tree.column("deposit", width=150, anchor=tk.CENTER)  # Equal width
        self.tree.column("from_account", width=150, anchor=tk.CENTER)
        self.tree.column("withdrawal", width=150, anchor=tk.CENTER)  # Equal width
        self.tree.column("to_account", width=150, anchor=tk.CENTER)
        self.tree.column("description", width=200, anchor=tk.CENTER)
        self.tree.column("balance", width=150, anchor=tk.CENTER)
        
        # Set display order of columns
        self.tree["displaycolumns"] = ("date", "deposit", "from_account", "withdrawal", "to_account", "description", "balance")
        
        # Add row colors
        self.tree.tag_configure('deposit', foreground="green")  # Light green for deposits
        self.tree.tag_configure('withdrawal', foreground="red")  # Light red for withdrawals
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Message when no results found
        self.no_results_label = Label(table_frame, text="No results found", 
                                     font=("Arial", 16), fg='#7f8c8d', bg='white')
        
        # Bind double-click event
        self.tree.bind("<Double-1>", self.on_item_double_click)
        
        # Statistics frame
        stats_frame = Frame(main_frame, bg='#f0f0f0')
        stats_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.stats_var = tk.StringVar()
        stats_label = Label(stats_frame, textvariable=self.stats_var, 
                           font=("Arial", 11), bg='#f0f0f0', fg='#2c3e50')
        stats_label.pack(side=tk.LEFT)
    
    def delete_transaction(self):
        """Delete selected transaction after passcode confirmation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return
        
        item = self.tree.item(selected[0])
        values = item["values"]
        
        # Find the original transaction in the list using a unique identifier
        date = values[0]
        deposit = values[1]
        withdrawal = values[3]
        description = values[5]
        
        # Determine the amount and type
        amount = float(deposit.replace(",", "")) if deposit != "0.00" else float(withdrawal.replace(",", ""))
        transaction_type = "Deposit" if deposit != "0.00" else "Withdrawal"
        
        # Find the exact transaction
        original_transaction = None
        index = -1
        
        for i, transaction in enumerate(self.transactions):
            if (transaction["date"] == date and 
                transaction["amount"] == amount and 
                transaction["description"] == description and 
                transaction["type"] == transaction_type):
                original_transaction = transaction
                index = i
                break
        
        if not original_transaction:
            messagebox.showerror("Error", "Could not find the selected transaction")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete this {transaction_type.lower()} transaction?\n"
                                     f"Date: {date}\nAmount: {amount} SAR\nDescription: {description}")
        
        if not confirm:
            return
        
        # Verify passcode before deletion
        dialog = PasscodeDialog(self.root, "Confirm Deletion", "Enter your passcode to confirm deletion:")
        self.root.wait_window(dialog.top)
        
        if not dialog.result:
            return  # User cancelled
        
        # Load saved passcode
        saved_passcode = load_passcode()
        
        if dialog.result != saved_passcode:
            messagebox.showerror("Error", "Incorrect passcode. Deletion cancelled.")
            return
        
        # Remove the transaction
        deleted_transaction = self.transactions.pop(index)
        
        # Update the balance
        if deleted_transaction["type"] == "Deposit":
            self.balance -= deleted_transaction["amount"]
        else:
            self.balance += deleted_transaction["amount"]
        
        # Save data and update display
        self.save_data()
        self.update_display()
        messagebox.showinfo("Success", "Transaction deleted successfully")
    
    def edit_transaction(self):
        """Edit selected transaction"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to edit")
            return
        
        item = self.tree.item(selected[0])
        values = item["values"]
        
        # Find the original transaction in the list using a unique identifier
        # We'll use the combination of date, amount, and description to identify the transaction
        date = values[0]
        deposit = values[1]
        withdrawal = values[3]
        description = values[5]
        
        # Determine the amount and type
        amount = float(deposit.replace(",", "")) if deposit != "0.00" else float(withdrawal.replace(",", ""))
        transaction_type = "Deposit" if deposit != "0.00" else "Withdrawal"
        
        # Find the exact transaction
        original_transaction = None
        index = -1
        
        for i, transaction in enumerate(self.transactions):
            if (transaction["date"] == date and 
                transaction["amount"] == amount and 
                transaction["description"] == description and 
                transaction["type"] == transaction_type):
                original_transaction = transaction
                index = i
                break
        
        if not original_transaction:
            messagebox.showerror("Error", "Could not find the selected transaction")
            return
        
        # Open edit dialog with current values
        dialog = EditTransactionDialog(self.root, original_transaction)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            # Get the updated values
            updated_amount, updated_from, updated_to, updated_desc = dialog.result
            
            # Validate amount
            try:
                updated_amount = float(updated_amount)
                if updated_amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero")
                    return
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return
            
            # Calculate the difference in balance
            old_amount = original_transaction["amount"]
            amount_difference = 0
            
            if original_transaction["type"] == "Deposit":
                amount_difference = updated_amount - old_amount
            else:
                amount_difference = old_amount - updated_amount
            
            # Check if withdrawal exceeds balance
            if original_transaction["type"] == "Withdrawal" and updated_amount > (self.balance + old_amount):
                messagebox.showerror("Error", "Insufficient balance for this withdrawal amount")
                return
            
            # Update the transaction
            self.transactions[index]["amount"] = updated_amount
            self.transactions[index]["from_account"] = updated_from
            self.transactions[index]["to_account"] = updated_to
            self.transactions[index]["description"] = updated_desc
            
            # Update the balance
            if original_transaction["type"] == "Deposit":
                self.balance += amount_difference
            else:
                self.balance += amount_difference
            
            # Save data and update display
            self.save_data()
            self.update_display()
            messagebox.showinfo("Success", "Transaction updated successfully")
    
    def filter_by_operation(self, event=None):
        """Filter transactions by selected operation type"""
        operation = self.operation_var.get()
        
        if operation == "All":
            self.update_display()
        elif operation == "Deposit only":
            deposits = [t for t in self.transactions if t["type"] == "Deposit"]
            self.update_display(deposits)
        elif operation == "Withdrawal only":
            withdrawals = [t for t in self.transactions if t["type"] == "Withdrawal"]
            self.update_display(withdrawals)
    
    def format_currency(self, amount):
        """Format amount with thousand separators"""
        try:
            return "{:,.2f}".format(float(amount))
        except:
            return "0.00"
    
    def add_deposit(self):
        self.add_transaction("Deposit")
    
    def add_withdrawal(self):
        self.add_transaction("Withdrawal")
    
    def add_transaction(self, transaction_type):
        dialog = EnhancedTransactionDialog(self.root, transaction_type)
        self.root.wait_window(dialog.top)
        
        if dialog.result:
            amount, from_account, to_account, description = dialog.result
            
            # Validate amount
            try:
                amount = float(amount)
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be greater than zero")
                    return
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number")
                return
            
            # Create transaction
            transaction = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "type": transaction_type,
                "amount": amount,
                "from_account": from_account,
                "to_account": to_account,
                "description": description
            }
            
            # Add transaction to list and update balance
            self.transactions.append(transaction)
            
            if transaction_type == "Deposit":
                self.balance += amount
            else:
                if amount > self.balance:
                    messagebox.showerror("Error", "Insufficient balance for withdrawal")
                    self.transactions.pop()
                    return
                self.balance -= amount
            
            # Save data and update display
            self.save_data()
            self.update_display()
            messagebox.showinfo("Success", f"{transaction_type} completed successfully")
    
    def calculate_running_balance(self):
        """Calculate running balance for each transaction"""
        running_balance = 0
        balances = []
        
        for transaction in self.transactions:
            if transaction["type"] == "Deposit":
                running_balance += transaction["amount"]
            else:
                running_balance -= transaction["amount"]
            balances.append(running_balance)
        
        return balances
    
    def calculate_account_balance(self, account_name):
        """Calculate balance for a specific account based on all transactions"""
        total_balance = 0
        
        for transaction in self.transactions:
            # Calculate deposits made by the account (credit)
            if transaction["type"] == "Deposit" and transaction.get("from_account") == account_name:
                total_balance += transaction["amount"]
            
            # Calculate withdrawals made to the account (debit)
            if transaction["type"] == "Withdrawal" and transaction.get("to_account") == account_name:
                total_balance -= transaction["amount"]
        
        return total_balance
    
    def quick_search(self, *args):
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.update_display()
            self.search_results_frame.pack_forget()
            return
        
        results = []
        for transaction in self.transactions:
            # Search in sender or receiver name
            from_match = "from_account" in transaction and search_term.lower() in transaction["from_account"].lower()
            to_match = "to_account" in transaction and search_term.lower() in transaction["to_account"].lower()
            desc_match = "description" in transaction and search_term.lower() in transaction["description"].lower()
            if from_match or to_match or desc_match:
                results.append(transaction)
        
        if results:
            self.update_display(results)
            
            # Calculate account's balance
            account_balance = self.calculate_account_balance(search_term)
            
            self.search_results_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Show balance
            self.search_results_var.set(
                f"Search results for '{search_term}': "
                f"Found {len(results)} transactions | "
                f"Balance: {self.format_currency(account_balance)} SAR"
            )
        else:
            self.update_display([])
            self.search_results_frame.pack(fill=tk.X, pady=(0, 15))
            self.search_results_var.set(f"No results found for '{search_term}'")
    
    def on_item_double_click(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            
            # Correct order of values according to displayed columns
            date = values[0]
            deposit = values[1]
            from_account = values[2]
            withdrawal = values[3]
            to_account = values[4]
            description = values[5]
            balance = values[6]
            
            transaction_type = "Deposit" if deposit != "0.00" else "Withdrawal"
            amount = deposit if deposit != "0.00" else withdrawal
            
            details = (f"Date: {date}\n"
                      f"Type: {transaction_type}\n"
                      f"Amount: {amount} SAR\n"
                      f"From: {from_account}\n"
                      f"To: {to_account}\n"
                      f"Description: {description}\n"
                      f"Balance after transaction: {balance} SAR")
            
            messagebox.showinfo("Transaction Details", details)
    
    def update_display(self, transactions=None):
        # Clear current table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Display transactions (or specified transactions in case of search)
        display_data = transactions if transactions is not None else self.transactions
        
        if display_data:
            self.no_results_label.pack_forget()
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Calculate running balance
            running_balances = self.calculate_running_balance()
            
            for i, transaction in enumerate(display_data):
                tag = 'deposit' if transaction['type'] == 'Deposit' else 'withdrawal'
                
                # Determine deposit and withdrawal values
                deposit_value = self.format_currency(transaction['amount']) if transaction['type'] == 'Deposit' else "0.00"
                withdrawal_value = self.format_currency(transaction['amount']) if transaction['type'] == 'Withdrawal' else "0.00"
                
                # Use appropriate running balance
                if transactions is None:
                    balance_value = self.format_currency(running_balances[i])
                else:
                    # In case of search, calculate balance based on displayed transactions only
                    temp_balance = 0
                    for j in range(i + 1):
                        if display_data[j]["type"] == "Deposit":
                            temp_balance += display_data[j]["amount"]
                        else:
                            temp_balance -= display_data[j]["amount"]
                    balance_value = self.format_currency(temp_balance)
                
                # Insert values in correct column order
                self.tree.insert("", "end", values=(
                    transaction["date"],
                    deposit_value,
                    transaction.get("from_account", "Not specified"),
                    withdrawal_value,
                    transaction.get("to_account", "Not specified"),
                    transaction["description"],
                    balance_value
                ), tags=(tag,))
        else:
            self.tree.pack_forget()
            self.no_results_label.pack(expand=True)
        
        # Update current balance
        self.balance_var.set(f"{self.format_currency(self.balance)} SAR")
        
        # Update statistics
        if transactions is None:
            total_deposits = sum(t['amount'] for t in self.transactions if t['type'] == 'Deposit')
            total_withdrawals = sum(t['amount'] for t in self.transactions if t['type'] == 'Withdrawal')
            
            display_count = len(self.transactions)
            self.stats_var.set(f"Showing {display_count} transactions | "
                              f"Total Deposits: {self.format_currency(total_deposits)} SAR | "
                              f"Total Withdrawals: {self.format_currency(total_withdrawals)} SAR")
        else:
            self.stats_var.set(f"Showing {len(display_data)} transactions from search results")
    
    def load_data(self):
        self.transactions = load_transactions()
        # Calculate current balance from transactions
        self.balance = 0.0
        for transaction in self.transactions:
            if transaction["type"] == "Deposit":
                self.balance += transaction["amount"]
            else:
                self.balance -= transaction["amount"]
    
    def save_data(self):
        save_transactions(self.transactions, self.balance)