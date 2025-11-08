"""
AdGenius AI Backend - Logging Utilities
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request

def setup_logger(app: Flask):
    """
    Setup application logger
    
    Args:
        app (Flask): Flask application
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(app.config['LOG_FILE'])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set log level
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    
    # Configure Flask logger
    handler = RotatingFileHandler(
        app.config['LOG_FILE'],
        maxBytes=10000000,  # 10MB
        backupCount=5
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to Flask logger
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)
    
    # Add console handler in development mode
    if app.debug:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        app.logger.addHandler(console_handler)
        root_logger.addHandler(console_handler)
    
    # Log requests
    @app.before_request
    def log_request_info():
        app.logger.debug('Request: %s %s', request.method, request.path)
    
    # Log responses
    @app.after_request
    def log_response_info(response):
        app.logger.debug('Response: %s', response.status)
        return response
    
    app.logger.info('Logger initialized')
