"""Risk evaluation endpoints."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import RiskEvaluationRequest, RiskEvaluationResponse
from app.utils.security_utils import calculate_transaction_risk, detect_scam_phrases

risk_bp = Blueprint("risk", __name__, url_prefix="/api/risk")


@risk_bp.route("/evaluate", methods=["POST"])
def evaluate_risk():
    """Evaluate risk for a transaction."""
    try:
        data = request.get_json()
        
        transcript = data.get("transcript", "").strip()
        amount = data.get("amount", 0)
        is_liveness_passed = data.get("is_liveness_passed", False)
        stress_level = data.get("stress_level", "low")
        
        if not transcript:
            return jsonify({"error": "transcript required"}), 400
        
        # Calculate risk
        result = calculate_transaction_risk(
            amount=amount,
            transcript=transcript,
            is_liveness_passed=is_liveness_passed,
            stress_level=stress_level,
        )
        
        # Add recommendations
        recommendations = []
        if result["risk_level"] == "CRITICAL":
            recommendations.append("Block transaction - extreme risk detected")
            recommendations.append("Contact customer support immediately")
        elif result["risk_level"] == "HIGH":
            recommendations.append("Request additional verification (OTP/2FA)")
            recommendations.append("Confirm transaction details with customer")
        elif result["risk_level"] == "MEDIUM":
            recommendations.append("Request verification code")
        else:
            recommendations.append("Proceed with transaction")
        
        result["recommendations"] = recommendations
        
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat(),
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@risk_bp.route("/scam-check", methods=["POST"])
def scam_check():
    """Check for scam phrases in text."""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "text required"}), 400
        
        result = detect_scam_phrases(text)
        return jsonify({
            **result,
            "timestamp": datetime.now().isoformat(),
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
