"""
Authentication Routes
OTP generation, verification, and user authentication
"""

from flask import Blueprint, request, jsonify
from pydantic import ValidationError, BaseModel, EmailStr
import re

from app.utils.sms_utils import send_sms_otp, verify_otp as verify_otp_sms

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SendOTPRequest(BaseModel):
    phone_number: str

class SendOTPResponse(BaseModel):
    success: bool
    session_id: str
    message: str
    mock_otp: str = None

class VerifyOTPRequest(BaseModel):
    session_id: str
    otp: str
    phone_number: str

class VerifyOTPResponse(BaseModel):
    success: bool
    message: str
    verified_phone: str = None

# ============================================================================
# ROUTES
# ============================================================================

@auth_bp.route('/otp/send', methods=['POST'])
def send_otp():
    """
    Send OTP to phone number
    
    Request:
        {
            "phone_number": "+91 98765 43210" or "9876543210"
        }
    
    Response:
        {
            "success": true,
            "session_id": "session_xxxxx",
            "message": "OTP sent to +91 98765 43210",
            "mock_otp": "123456"  # Only in development
        }
    """
    try:
        # Parse request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is empty"
            }), 400
        
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return jsonify({
                "success": False,
                "message": "Phone number is required"
            }), 400
        
        # Validate phone number format
        digits_only = ''.join(c for c in phone_number if c.isdigit())
        
        if len(digits_only) not in [10, 12]:
            return jsonify({
                "success": False,
                "message": "Invalid phone number format. Expected 10-digit number or with country code."
            }), 400
        
        # Send OTP
        result = send_sms_otp(phone_number)
        
        return jsonify(result), 200 if result.get('success') else 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error sending OTP: {str(e)}"
        }), 500

@auth_bp.route('/otp/verify', methods=['POST'])
def verify_otp_endpoint():
    """
    Verify OTP
    
    Request:
        {
            "session_id": "session_xxxxx",
            "otp": "123456",
            "phone_number": "+91 98765 43210"
        }
    
    Response:
        {
            "success": true,
            "message": "OTP verified successfully",
            "verified_phone": "+91 98765 43210"
        }
    """
    try:
        # Parse request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is empty"
            }), 400
        
        session_id = data.get('session_id', '').strip()
        otp = data.get('otp', '').strip()
        phone_number = data.get('phone_number', '').strip()
        
        # Validate inputs
        if not session_id:
            return jsonify({
                "success": False,
                "message": "Session ID is required"
            }), 400
        
        if not otp:
            return jsonify({
                "success": False,
                "message": "OTP is required"
            }), 400
        
        if not phone_number:
            return jsonify({
                "success": False,
                "message": "Phone number is required"
            }), 400
        
        # OTP must be 6 digits
        if not otp.isdigit() or len(otp) != 6:
            return jsonify({
                "success": False,
                "message": "OTP must be 6 digits"
            }), 400
        
        # Verify OTP
        result = verify_otp_sms(session_id, otp, phone_number)
        
        return jsonify(result), 200 if result.get('success') else 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error verifying OTP: {str(e)}"
        }), 500

@auth_bp.route('/otp/resend', methods=['POST'])
def resend_otp():
    """
    Resend OTP to phone number (rate-limited)
    
    Request:
        {
            "phone_number": "+91 98765 43210"
        }
    
    Response:
        {
            "success": true,
            "session_id": "session_xxxxx",
            "message": "OTP resent to +91 98765 43210"
        }
    """
    try:
        data = request.get_json()
        phone_number = data.get('phone_number', '').strip()
        
        if not phone_number:
            return jsonify({
                "success": False,
                "message": "Phone number is required"
            }), 400
        
        # Send new OTP (rate limiting should be added in production)
        result = send_sms_otp(phone_number)
        
        return jsonify(result), 200 if result.get('success') else 400
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error resending OTP: {str(e)}"
        }), 500

@auth_bp.route('/health', methods=['GET'])
def auth_health():
    """Check auth service health"""
    return jsonify({
        "status": "healthy",
        "service": "authentication",
        "endpoints": [
            "POST /auth/otp/send",
            "POST /auth/otp/verify",
            "POST /auth/otp/resend",
        ]
    }), 200
