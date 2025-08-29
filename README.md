# Personal Account Statement

A simple desktop app to record your income and expenses.

## Features
- Add, edit, and delete deposits and withdrawals
- Automatic balance calculation
- Quick search for transactions
- Data saved automatically

## How to Run

### Option 1: With Python
1. Install [Python](https://www.python.org/downloads/) (3.6 or newer).
2. Download all project files into one folder.
3. Run:
```bash
python main.py
```

### Option 2: Create an Executable (.exe)
1. Install PyInstaller:
```bash
pip install pyinstaller
```
2. Run inside the project folder:
```bash
python -m PyInstaller --onefile --windowed --icon=assets\icons\app.ico --name "Personal Account Statement" main.py
```
3. After build, the file will be here:
```
dist/Personal Account Statement.exe
```
4. Copy the folders **data** and **assets** next to the `.exe` file.
5. Right-click the `.exe` → Pin to taskbar (for quick access).

## Usage
- First time: set a 4-digit PIN.
- Add income with "New Deposit".
- Add expenses with "New Withdrawal".
- Double-click a transaction to see details.
- Your balance is shown at the top.

## Project Structure
- **main.py** → App entry point  
- **core/** → Main logic  
- **utils/** → Helper functions  
- **dialogs/** → Pop-up windows  
- **data/** → User data  
- **assets/** → Icons and resources  

## Requirements
- Python 3.6+ (if running directly)  
- PyInstaller (only if building `.exe`)  

## Security
- Local data only  
- Simple PIN protection  

## Note
This app is for **personal use only**. It is not intended for business or professional accounting.
