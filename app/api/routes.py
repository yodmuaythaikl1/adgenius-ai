"""
AdGenius AI Backend - API Routes
"""
from flask import Blueprint, Flask, jsonify

# Import API modules
from app.api.auth import auth_bp
from app.api.campaigns import campaigns_bp
from app.api.analytics import analytics_bp
from app.api.users import users_bp

def register_routes(app: Flask):
    """
    Register API routes with Flask application
    
    Args:
        app (Flask): Flask application
    """
    # Create main API blueprint
    api_bp = Blueprint('api', __name__, url_prefix=app.config['API_PREFIX'])
    
    # Register API module blueprints
    api_bp.register_blueprint(auth_bp)
    api_bp.register_blueprint(campaigns_bp)
    api_bp.register_blueprint(analytics_bp)
    api_bp.register_blueprint(users_bp)
    
    # Register main API blueprint with app
    app.register_blueprint(api_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            "name": "AdGenius AI API",
            "version": "1.0.0",
            "status": "running"
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy"
        })
