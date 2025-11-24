from flask import Flask
from flask_cors import CORS
from app.config import CORS_ORIGINS, SECRET_KEY
from app.routes import health_bp, voice_bp, banking_bp, risk_bp, auth_bp


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    
    # Enable CORS
    CORS(app, origins=CORS_ORIGINS)
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(banking_bp)
    app.register_blueprint(risk_bp)
    app.register_blueprint(auth_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500
    
    return app

