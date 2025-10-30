from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

TRANSACTIONS_FILE = BASE_DIR / "core" / "data" / "transactions.json"
PASSCODE_FILE = BASE_DIR / "core" / "data" / "passcode.json"
APP_ICON = BASE_DIR / "assets" / "icons" / "app.ico"
APP_TITLE = "Personal Account Statement"
