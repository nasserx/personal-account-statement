import json
from pathlib import Path
from typing import Any, Dict, List
from core.config import TRANSACTIONS_FILE, PASSCODE_FILE

def load_json(file_path: Path) -> Any:
    """Load data from a JSON file"""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return None

def save_json(data: Any, file_path: Path) -> bool:
    """Save data to a JSON file"""
    try:
        file_path.parent.mkdir(exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving {file_path}: {e}")
        return False

def load_transactions() -> List[Dict]:
    """Load transactions"""
    data = load_json(TRANSACTIONS_FILE)
    return data.get("transactions", []) if data else []

def save_transactions(transactions: List[Dict], balance: float) -> bool:
    """Save transactions"""
    data = {
        "transactions": transactions,
        "balance": balance
    }
    return save_json(data, TRANSACTIONS_FILE)

def load_passcode() -> str:
    """Load passcode"""
    data = load_json(PASSCODE_FILE)
    return data.get("passcode", "") if data else ""

def save_passcode(passcode: str) -> bool:
    """Save passcode"""
    return save_json({"passcode": passcode}, PASSCODE_FILE)
