"""Voice processing endpoints."""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import VoiceTranscribeRequest, VoiceLivenessRequest, LivenessResponse
from app.utils.ml_utils import transcribe_audio, verify_speaker, detect_emotion, detect_scam_phrases
from app.utils.security_utils import validate_challenge

voice_bp = Blueprint("voice", __name__, url_prefix="/api/voice")


@voice_bp.route("/transcribe", methods=["POST"])
def transcribe():
    """Transcribe audio file using Whisper."""
    try:
        data = request.get_json()
        audio_file_path = data.get("audio_file_path")
        user_id = data.get("user_id", "user_123")
        
        if not audio_file_path:
            return jsonify({"error": "audio_file_path required"}), 400
        
        result = transcribe_audio(audio_file_path)
        
        if "error" in result:
            return jsonify(result), 400
        
        # Detect emotion from transcription
        emotion_result = detect_emotion(result["text"])
        
        # Detect scam phrases
        scam_result = detect_scam_phrases(result["text"])
        
        return jsonify({
            **result,
            "emotion": emotion_result,
            "scam_detection": scam_result,
            "timestamp": datetime.now().isoformat(),
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@voice_bp.route("/liveness", methods=["POST"])
def liveness_check():
    """Verify voice liveness using challenge-response."""
    try:
        data = request.get_json()
        transcript = data.get("transcript", "").strip()
        challenge_phrase = data.get("challenge_phrase", "").strip()
        user_id = data.get("user_id", "user_123")
        
        if not transcript or not challenge_phrase:
            return jsonify({"error": "transcript and challenge_phrase required"}), 400
        
        # Verify speaker using challenge response
        liveness_result = verify_speaker(transcript, challenge_phrase)
        
        # Detect stress level
        emotion = detect_emotion(transcript)
        
        # Combine results
        response = {
            **liveness_result,
            "stress_level": emotion["stress_level"],
            "timestamp": datetime.now().isoformat(),
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@voice_bp.route("/emotion", methods=["POST"])
def emotion():
    """Detect emotion and stress from text."""
    try:
        data = request.get_json()
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "text required"}), 400
        
        result = detect_emotion(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
