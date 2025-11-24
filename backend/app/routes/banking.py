"""Banking operation endpoints."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import TransactionRequest, BalanceResponse, TransactionResponse
from app.utils.banking_utils import (
    get_balance,
    get_transactions,
    execute_transfer,
    validate_transfer,
)
from app.utils.security_utils import calculate_transaction_risk

banking_bp = Blueprint("banking", __name__, url_prefix="/api/banking")


@banking_bp.route("/balance", methods=["GET"])
def balance():
    """Get account balance."""
    try:
        user_id = request.args.get("user_id", "user_123")
        result = get_balance(user_id)
        
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@banking_bp.route("/transactions", methods=["GET"])
def transactions():
    """Get recent transactions."""
    try:
        user_id = request.args.get("user_id", "user_123")
        limit = request.args.get("limit", 5, type=int)
        
        result = get_transactions(user_id, limit)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@banking_bp.route("/transfer", methods=["POST"])
def transfer():
    """Execute a bank transfer."""
    try:
        data = request.get_json()
        
        amount = data.get("amount")
        recipient_account = data.get("recipient_account")
        recipient_name = data.get("recipient_name")
        user_id = data.get("user_id", "user_123")
        
        if not all([amount, recipient_account, recipient_name]):
            return jsonify({"error": "amount, recipient_account, and recipient_name required"}), 400
        
        # Validate transfer
        validation = validate_transfer(amount, user_id)
        if not validation["valid"]:
            return jsonify({
                "success": False,
                "error": validation["reason"],
                "timestamp": datetime.now().isoformat(),
            }), 400
        
        # Execute transfer
        result = execute_transfer(user_id, amount, recipient_account, recipient_name)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@banking_bp.route("/transfer/validate", methods=["POST"])
def validate_transfer_endpoint():
    """Validate transfer before execution."""
    try:
        data = request.get_json()
        amount = data.get("amount")
        user_id = data.get("user_id", "user_123")
        
        if not amount:
            return jsonify({"error": "amount required"}), 400
        
        result = validate_transfer(amount, user_id)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
