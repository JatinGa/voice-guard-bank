"""Security and validation utilities."""
import re
import hashlib
from datetime import datetime, timedelta

# List of scam/suspicious phrases
SCAM_PHRASES = [
    "account is blocked",
    "share otp",
    "kyc expired",
    "verification from bank",
    "urgent action required",
    "account suspended",
    "confirm your details",
    "update your password",
    "click this link",
    "verify identity",
    "click here immediately",
    "unusual activity detected",
]

# Challenge phrases for liveness verification
LIVENESS_CHALLENGES = [
    "green mango",
    "blue river",
    "silver coin",
    "seven eight nine",
    "bright sun",
    "warm cup",
    "strong tree",
    "deep water",
]


def validate_challenge(transcript: str, challenge_phrase: str) -> dict:
    """
    Validate if transcript contains the challenge phrase.
    Returns confidence score and whether verification passed.
    """
    transcript_normalized = transcript.lower().strip()
    challenge_normalized = challenge_phrase.lower().strip()
    
    score = 0
    
    # Direct match (100 points)
    if transcript_normalized == challenge_normalized:
        score = 100
    # Contains all words
    elif all(word in transcript_normalized for word in challenge_normalized.split()):
        score = 80
    # Contains phrase as substring
    elif challenge_normalized in transcript_normalized:
        score = 75
    # Partial word match
    elif any(word in transcript_normalized for word in challenge_normalized.split()):
        score = 50
    # No match
    else:
        score = 0
    
    passed = score >= 70
    
    return {
        "passed": passed,
        "score": score,
        "confidence": score / 100,
    }


def detect_scam_phrases(text: str) -> dict:
    """
    Detect known scam phrases in text.
    """
    text_lower = text.lower()
    detected = []
    
    for phrase in SCAM_PHRASES:
        if phrase in text_lower:
            detected.append(phrase)
    
    risk_score = min(len(detected) * 25, 100)
    
    return {
        "detected": len(detected) > 0,
        "phrases": detected,
        "count": len(detected),
        "risk_score": risk_score,
    }


def calculate_transaction_risk(
    amount: float,
    transcript: str,
    is_liveness_passed: bool,
    stress_level: str,
) -> dict:
    """
    Calculate overall risk score for a transaction.
    
    Factors:
    - Amount (larger amounts = higher risk)
    - Scam phrases detected
    - Liveness verification passed
    - Stress/emotion indicators
    """
    risk_score = 0
    factors = []
    
    # Amount-based risk (0-30 points)
    if amount > 100000:
        risk_score += 30
        factors.append("High-value transfer (>₹100k)")
    elif amount > 50000:
        risk_score += 20
        factors.append("Medium-high value transfer (>₹50k)")
    elif amount > 10000:
        risk_score += 10
        factors.append("Medium value transfer (>₹10k)")
    
    # Scam phrase detection (0-40 points)
    scam_check = detect_scam_phrases(transcript)
    risk_score += scam_check["risk_score"]
    if scam_check["detected"]:
        factors.append(f"Scam phrases detected: {', '.join(scam_check['phrases'])}")
    
    # Liveness verification (0-20 points)
    if not is_liveness_passed:
        risk_score += 20
        factors.append("Failed voice liveness verification")
    
    # Stress indicators (0-10 points)
    if stress_level == "high":
        risk_score += 10
        factors.append("High stress detected in voice")
    elif stress_level == "medium":
        risk_score += 5
        factors.append("Moderate stress detected")
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "CRITICAL"
    elif risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "factors": factors,
        "requires_additional_verification": risk_score >= 50,
    }


def generate_otp(length: int = 6) -> str:
    """Generate a random OTP."""
    import random
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def hash_password(password: str) -> str:
    """Hash password for storage (simplified - use bcrypt in production)."""
    return hashlib.sha256(password.encode()).hexdigest()
