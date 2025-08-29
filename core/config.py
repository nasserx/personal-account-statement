from pathlib import Path

# Data and directories 
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)  # Create the folder if it does not exist

ASSETS_DIR = Path("assets")
ICONS_DIR = ASSETS_DIR / "icons"

# Data files 
TRANSACTIONS_FILE = DATA_DIR / "transactions.json"
PASSCODE_FILE = DATA_DIR / "passcode.json"

# Application settings 
APP_TITLE = "Personal Account Statement"
APP_ICON = ICONS_DIR / "app.ico"
