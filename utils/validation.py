from pathlib import Path

def validate_path(path: str, should_exist: bool = True) -> bool:
    """Validate the path"""
    try:
        path_obj = Path(path)
        if should_exist:
            return path_obj.exists()
        return True
    except Exception:
        return False

def validate_icon_path(icon_path: str) -> bool:
    """Check if icon exists"""
    return validate_path(icon_path, should_exist=True)

def validate_amount(amount_str: str) -> tuple[bool, float]:
    """Validate the amount"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, 0.0
        return True, amount
    except ValueError:
        return False, 0.0

def validate_passcode(passcode: str) -> bool:
    """Validate the passcode"""
    return len(passcode) == 4 and passcode.isdigit()

def validate_required_fields(*fields) -> bool:
    """Check that all required fields are filled"""
    return all(field.strip() for field in fields)
