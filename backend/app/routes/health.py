"""Health check endpoints."""
from flask import Blueprint
from datetime import datetime
from app.models import HealthResponse

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "message": "SentinelPay backend is running",
        "timestamp": datetime.now().isoformat(),
    }


@health_bp.route("/status", methods=["GET"])
def status():
    """Detailed status endpoint."""
    return {
        "status": "running",
        "service": "SentinelPay Backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "voice_transcription",
            "voice_liveness",
            "risk_evaluation",
            "transaction_execution",
            "banking_operations",
        ],
    }
