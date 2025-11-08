"""
AdGenius AI Backend - Configuration Settings
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    
    # API settings
    API_PREFIX = os.getenv('API_PREFIX', '/api/v1')
    
    # MongoDB settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/adgenius_ai')
    MONGODB_SETTINGS = {
        'host': MONGODB_URI
    }
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400))
    )
    
    # Facebook API settings
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    FACEBOOK_API_VERSION = os.getenv('FACEBOOK_API_VERSION', 'v16.0')
    
    # Instagram API settings (uses Facebook API)
    INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
    
    # TikTok API settings
    TIKTOK_APP_ID = os.getenv('TIKTOK_APP_ID')
    TIKTOK_APP_SECRET = os.getenv('TIKTOK_APP_SECRET')
    TIKTOK_API_VERSION = os.getenv('TIKTOK_API_VERSION', 'v1.3')
    
    # Shopee API settings
    SHOPEE_PARTNER_ID = os.getenv('SHOPEE_PARTNER_ID')
    SHOPEE_PARTNER_KEY = os.getenv('SHOPEE_PARTNER_KEY')
    SHOPEE_API_URL = os.getenv('SHOPEE_API_URL', 'https://partner.shopeemobile.com')
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Redis settings
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/adgenius_ai.log')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_URI = os.getenv('TEST_MONGODB_URI', 'mongodb://localhost:27017/adgenius_ai_test')
    MONGODB_SETTINGS = {
        'host': MONGODB_URI
    }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Additional production-specific settings

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
