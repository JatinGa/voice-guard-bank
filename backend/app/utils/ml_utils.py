"""Machine learning utilities for voice processing."""
import os
import io
import whisper
import numpy as np
from app.config import WHISPER_MODEL, DEVICE

# Global model cache
_whisper_model = None
_emotion_model = None

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
]

FILLER_WORDS = ["uh", "um", "ah", "uh-huh", "like", "you know", "basically", "literally"]


def load_models():
    """Load ML models on demand."""
    global _whisper_model
    if _whisper_model is None:
        print(f"Loading Whisper model ({WHISPER_MODEL}) on {DEVICE}...")
        _whisper_model = whisper.load_model(WHISPER_MODEL, device=DEVICE)
    return _whisper_model


def transcribe_audio(audio_file_path: str) -> dict:
    """
    Transcribe audio using OpenAI Whisper.
    
    Args:
        audio_file_path: Path to audio file
        
    Returns:
        {
            "text": "transcribed text",
            "language": "detected language code",
            "duration": duration_in_seconds,
            "confidence": confidence_score
        }
    """
    try:
        model = load_models()
        result = model.transcribe(audio_file_path, language="en")
        
        return {
            "text": result["text"].strip(),
            "language": result.get("language", "en"),
            "duration": result.get("duration", 0),
            "confidence": float(result.get("segments", [{}])[0].get("confidence", 0.5)),
        }
    except Exception as e:
        print(f"Transcription error: {e}")
        return {"text": "", "error": str(e), "confidence": 0}


def verify_speaker(transcript: str, challenge_phrase: str) -> dict:
    """
    Verify speaker using challenge-response pattern matching.
    Enhanced with ML for future speaker verification.
    
    Args:
        transcript: User's spoken response
        challenge_phrase: Challenge phrase that was asked
        
    Returns:
        {
            "passed": bool,
            "score": 0-100,
            "reasons": [list of factors],
            "confidence": 0-1
        }
    """
    transcript_lower = transcript.lower().strip()
    challenge_lower = challenge_phrase.lower().strip()
    
    score = 50  # Base score
    reasons = []
    
    # Check for challenge phrase match (40 points)
    if challenge_lower in transcript_lower:
        score += 40
        reasons.append(f"Challenge phrase '{challenge_phrase}' detected")
    elif any(word in transcript_lower for word in challenge_lower.split()):
        score += 25
        reasons.append(f"Partial match with challenge phrase")
    else:
        score -= 20
        reasons.append(f"Challenge phrase not detected")
    
    # Count filler words (-5 points each)
    filler_count = sum(1 for word in FILLER_WORDS if f" {word} " in f" {transcript_lower} ")
    if filler_count > 0:
        score -= (filler_count * 5)
        reasons.append(f"Filler words detected: {filler_count}")
    
    # Check for natural speech patterns (+5 points)
    if len(transcript.split()) >= 3:
        score += 5
        reasons.append("Natural speech pattern detected")
    
    # Ensure score is in valid range
    score = max(0, min(100, score))
    passed = score >= 70
    
    return {
        "passed": passed,
        "score": score,
        "reasons": reasons,
        "confidence": min(score / 100, 1.0),
        "transcript": transcript,
    }


def detect_emotion(text: str) -> dict:
    """
    Detect emotion/stress from text using sentiment analysis.
    (Simplified version - can be replaced with SpeechBrain model)
    
    Args:
        text: Transcribed text
        
    Returns:
        {
            "stress_level": "low" | "medium" | "high",
            "confidence": 0-1,
            "emotions": {"fear": score, "urgency": score, ...}
        }
    """
    text_lower = text.lower()
    
    # Simple keyword-based stress detection
    stress_keywords = {
        "urgent": 3,
        "immediately": 3,
        "emergency": 3,
        "quick": 2,
        "hurry": 2,
        "please": 1,
        "help": 2,
        "worried": 2,
        "confused": 1,
    }
    
    stress_score = sum(score for keyword, score in stress_keywords.items() if keyword in text_lower)
    stress_level = "high" if stress_score >= 4 else "medium" if stress_score >= 2 else "low"
    
    return {
        "stress_level": stress_level,
        "confidence": min(stress_score / 10, 1.0),
        "emotions": {
            "urgency": min(stress_score / 10, 1.0),
            "fear": 0.2 if "help" in text_lower else 0.0,
        },
        "raw_score": stress_score,
    }


def detect_scam_phrases(text: str) -> dict:
    """
    Detect known scam phrases in text.
    
    Args:
        text: Transcribed text
        
    Returns:
        {
            "is_scam_suspected": bool,
            "detected_phrases": [list of detected phrases],
            "confidence": 0-1
        }
    """
    text_lower = text.lower()
    detected = []
    
    for phrase in SCAM_PHRASES:
        if phrase in text_lower:
            detected.append(phrase)
    
    is_scam = len(detected) > 0
    confidence = min(len(detected) * 0.3, 1.0) if is_scam else 0.0
    
    return {
        "is_scam_suspected": is_scam,
        "detected_phrases": detected,
        "confidence": confidence,
    }
