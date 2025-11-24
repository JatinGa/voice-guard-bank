"""Banking operation utilities."""
import random
import string
from datetime import datetime, timedelta

# Mock bank account database
MOCK_ACCOUNTS = {
    "user_123": {
        "account_number": "9876543210",
        "balance": 45230.50,
        "currency": "INR",
    }
}

MOCK_TRANSACTIONS = {
    "user_123": [
        {
            "id": "txn_001",
            "description": "Groceries",
            "amount": 850.00,
            "date": "2025-11-20T10:30:00Z",
            "balance_after": 45230.50,
        },
        {
            "id": "txn_002",
            "description": "Gas Station",
            "amount": 500.00,
            "date": "2025-11-19T15:45:00Z",
            "balance_after": 46080.50,
        },
        {
            "id": "txn_003",
            "description": "Restaurant",
            "amount": 1200.00,
            "date": "2025-11-18T20:15:00Z",
            "balance_after": 46580.50,
        },
        {
            "id": "txn_004",
            "description": "Online Shopping",
            "amount": 2450.00,
            "date": "2025-11-17T09:00:00Z",
            "balance_after": 47780.50,
        },
        {
            "id": "txn_005",
            "description": "Mobile Bill",
            "amount": 499.00,
            "date": "2025-11-16T14:20:00Z",
            "balance_after": 50230.50,
        },
    ]
}


def get_balance(user_id: str = "user_123") -> dict:
    """Get account balance."""
    if user_id in MOCK_ACCOUNTS:
        account = MOCK_ACCOUNTS[user_id]
        return {
            "account_number": account["account_number"],
            "balance": account["balance"],
            "currency": account["currency"],
            "timestamp": datetime.now().isoformat(),
        }
    return {"error": "Account not found"}


def get_transactions(user_id: str = "user_123", limit: int = 5) -> dict:
    """Get recent transactions."""
    if user_id in MOCK_TRANSACTIONS:
        transactions = MOCK_TRANSACTIONS[user_id][:limit]
        return {
            "transactions": transactions,
            "count": len(transactions),
            "timestamp": datetime.now().isoformat(),
        }
    return {"transactions": [], "count": 0}


def execute_transfer(
    user_id: str,
    amount: float,
    recipient_account: str,
    recipient_name: str,
) -> dict:
    """Execute a mock bank transfer."""
    if user_id not in MOCK_ACCOUNTS:
        return {"success": False, "error": "Account not found"}
    
    account = MOCK_ACCOUNTS[user_id]
    
    if account["balance"] < amount:
        return {"success": False, "error": f"Insufficient balance. Available: {account['balance']}"}
    
    # Deduct amount
    account["balance"] -= amount
    
    # Generate transaction ID
    txn_id = "TXN" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Create transaction record
    transaction = {
        "id": txn_id,
        "description": f"Transfer to {recipient_name}",
        "amount": amount,
        "recipient_account": recipient_account,
        "recipient_name": recipient_name,
        "date": datetime.now().isoformat(),
        "balance_after": account["balance"],
        "status": "completed",
    }
    
    # Add to transaction history
    if user_id not in MOCK_TRANSACTIONS:
        MOCK_TRANSACTIONS[user_id] = []
    MOCK_TRANSACTIONS[user_id].insert(0, transaction)
    
    return {
        "success": True,
        "transaction_id": txn_id,
        "amount": amount,
        "recipient": recipient_name,
        "new_balance": account["balance"],
        "message": f"Transfer of ₹{amount} to {recipient_name} successful",
        "timestamp": datetime.now().isoformat(),
    }


def validate_transfer(amount: float, user_id: str = "user_123") -> dict:
    """Validate transfer before execution."""
    if user_id not in MOCK_ACCOUNTS:
        return {"valid": False, "reason": "Account not found"}
    
    account = MOCK_ACCOUNTS[user_id]
    
    if amount <= 0:
        return {"valid": False, "reason": "Amount must be positive"}
    
    if amount > account["balance"]:
        return {"valid": False, "reason": f"Insufficient balance. Available: {account['balance']}"}
    
    if amount > 100000:
        return {"valid": True, "requires_verification": True, "reason": "High-value transfer requires additional verification"}
    
    return {"valid": True, "requires_verification": False}
