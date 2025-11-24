"""
SMS Sending Utility using Twilio
Send OTP and verification codes via SMS
"""

import os
import random
import string
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

# Try to import Twilio, but make it optional
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    TWILIO_AVAILABLE = False

# In-memory store for OTP sessions (replace with Redis/DB in production)
OTP_SESSIONS: Dict[str, Dict] = {}

def generate_otp(length: int = 6) -> str:
    """Generate a random OTP of specified length (digits only)"""
    return ''.join(random.choices(string.digits, k=length))

def send_sms_otp(phone_number: str) -> Dict:
    """
    Send OTP via SMS using Twilio
    
    Args:
        phone_number: Phone number in format +91XXXXXXXXXX or 10-digit number
        
    Returns:
        {
            "success": bool,
            "session_id": str,
            "message": str,
            "otp": str (only in non-production mode)
        }
    """
    
    # Normalize phone number
    phone = phone_number.strip()
    
    # Remove non-digit characters
    digits_only = ''.join(c for c in phone if c.isdigit())
    
    # Validate length
    if len(digits_only) == 10:
        # Indian number without country code
        phone = f"+91{digits_only}"
    elif len(digits_only) == 12:
        # Indian number with country code (91)
        phone = f"+{digits_only}"
    else:
        return {
            "success": False,
            "message": "Invalid phone number format. Expected 10-digit number.",
        }
    
    # Generate OTP
    otp = generate_otp(6)
    
    # Create session
    session_id = f"session_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # Store OTP in memory (expires in 5 minutes)
    expires_at = datetime.now() + timedelta(minutes=5)
    OTP_SESSIONS[session_id] = {
        "otp": otp,
        "phone": phone,
        "created_at": datetime.now().isoformat(),
        "expires_at": expires_at.isoformat(),
    }
    
    # Try to send via Twilio if available and configured
    if TWILIO_AVAILABLE and should_send_real_sms():
        try:
            client = Client(
                os.getenv("TWILIO_ACCOUNT_SID"),
                os.getenv("TWILIO_AUTH_TOKEN")
            )
            
            message = client.messages.create(
                body=f"Your SentinelPay verification code is: {otp}. Valid for 5 minutes.",
                from_=os.getenv("TWILIO_PHONE_NUMBER"),
                to=phone
            )
            
            return {
                "success": True,
                "session_id": session_id,
                "message": f"OTP sent to {phone}",
                "twilio_sid": message.sid,
            }
        except Exception as e:
            print(f"Twilio SMS failed: {str(e)}")
            # Fall back to mock SMS
            return send_mock_sms(phone, otp, session_id)
    else:
        # Use mock SMS (for development/testing)
        return send_mock_sms(phone, otp, session_id)

def send_mock_sms(phone: str, otp: str, session_id: str) -> Dict:
    """
    Mock SMS sending for development/testing
    In production, this should never show the actual OTP
    """
    is_production = os.getenv("ENVIRONMENT") == "production"
    
    print(f"[MOCK SMS] OTP sent to {phone}: {otp}")
    
    response = {
        "success": True,
        "session_id": session_id,
        "message": f"OTP sent to {phone} (mock mode)",
    }
    
    # Only include mock_otp in development
    if not is_production:
        response["mock_otp"] = otp  # For testing only
    
    return response

def verify_otp(session_id: str, otp: str, phone_number: str) -> Dict:
    """
    Verify OTP against the stored session
    
    Args:
        session_id: Session ID from send_otp
        otp: OTP entered by user
        phone_number: Phone number (for verification)
        
    Returns:
        {
            "success": bool,
            "message": str,
            "verified_phone": str (if successful)
        }
    """
    
    # Normalize phone number
    phone = phone_number.strip()
    digits_only = ''.join(c for c in phone if c.isdigit())
    
    if len(digits_only) == 10:
        phone = f"+91{digits_only}"
    elif len(digits_only) == 12:
        phone = f"+{digits_only}"
    
    # Check if session exists
    if session_id not in OTP_SESSIONS:
        return {
            "success": False,
            "message": "Session expired or not found. Please request a new OTP.",
        }
    
    session_data = OTP_SESSIONS[session_id]
    
    # Check if OTP is expired
    expires_at = datetime.fromisoformat(session_data["expires_at"])
    if datetime.now() > expires_at:
        del OTP_SESSIONS[session_id]
        return {
            "success": False,
            "message": "OTP expired. Please request a new OTP.",
        }
    
    # Verify OTP
    if otp != session_data["otp"]:
        return {
            "success": False,
            "message": "Invalid OTP. Please try again.",
        }
    
    # Verify phone number matches
    if phone != session_data["phone"]:
        return {
            "success": False,
            "message": "Phone number mismatch.",
        }
    
    # OTP verified successfully
    del OTP_SESSIONS[session_id]
    
    return {
        "success": True,
        "message": "OTP verified successfully",
        "verified_phone": phone,
    }

def should_send_real_sms() -> bool:
    """Check if all Twilio credentials are configured"""
    return all([
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN"),
        os.getenv("TWILIO_PHONE_NUMBER"),
    ])

def cleanup_expired_otps():
    """Remove expired OTP sessions (call periodically in production)"""
    now = datetime.now()
    expired_sessions = [
        session_id for session_id, data in OTP_SESSIONS.items()
        if datetime.fromisoformat(data["expires_at"]) < now
    ]
    
    for session_id in expired_sessions:
        del OTP_SESSIONS[session_id]
    
    return len(expired_sessions)
