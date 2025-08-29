import tkinter as tk
from core.app import ModernTransactionApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernTransactionApp(root)
    root.mainloop()