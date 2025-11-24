#!/usr/bin/env python3
"""Run the Flask application."""
import os
from app import create_app
from app.config import API_HOST, API_PORT, FLASK_ENV

if __name__ == "__main__":
    app = create_app()
    
    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║          SentinelPay Backend - Starting                ║
    ╚════════════════════════════════════════════════════════╝
    
    Environment: {FLASK_ENV}
    Host: {API_HOST}
    Port: {API_PORT}
    URL: http://{API_HOST if API_HOST != '0.0.0.0' else 'localhost'}:{API_PORT}
    
    Available endpoints:
    - GET  /api/health
    - GET  /api/status
    - POST /api/voice/transcribe
    - POST /api/voice/liveness
    - POST /api/voice/emotion
    - GET  /api/banking/balance
    - GET  /api/banking/transactions
    - POST /api/banking/transfer
    - POST /api/banking/transfer/validate
    - POST /api/risk/evaluate
    - POST /api/risk/scam-check
    
    Press CTRL+C to quit
    """)
    
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=(FLASK_ENV == "development"),
    )
