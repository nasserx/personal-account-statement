from datetime import datetime

def filter_transactions_by_date(transactions_list: list[dict], from_date: str, to_date: str) -> list[dict]:
    """
    Filter transactions by date range
    
    Args:
        transactions_list: List of transaction dictionaries
        from_date: Start date in format "YYYY-MM-DD"
        to_date: End date in format "YYYY-MM-DD"
    
    Returns:
        Filtered list of transactions within the date range
    """
    if not transactions_list:
        return []
    
    try:
        start = datetime.strptime(from_date, "%Y-%m-%d").date()
        end = datetime.strptime(to_date, "%Y-%m-%d").date()
        
        filtered_transactions = []
        
        for transaction in transactions_list:
            transaction_date = datetime.strptime(transaction["date"], "%Y-%m-%d").date()
            if start <= transaction_date <= end:
                filtered_transactions.append(transaction)
        
        return filtered_transactions
    
    except ValueError:
        # Return empty list if date format is invalid
        return []