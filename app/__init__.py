"""
AdGenius AI Backend - Flask Application Factory
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from app.config import config_by_name
from app.utils.logger import setup_logger

# Import API routes
from app.api.routes import register_routes

def create_app(config_name="development"):
    """
    Create Flask application with specified configuration
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Setup CORS
    CORS(app)
    
    # Setup JWT
    JWTManager(app)
    
    # Setup logger
    setup_logger(app)
    
    # Register API routes
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """
    Register error handlers for the application
    
    Args:
        app (Flask): Flask application
    """
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return {"error": "Internal server error"}, 500
