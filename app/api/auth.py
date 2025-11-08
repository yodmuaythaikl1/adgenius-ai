"""
AdGenius AI Backend - Authentication API
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_password, validate_required_fields

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create auth service
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Returns:
        Response: JSON response
    """
    data = request.get_json()
    
    # Validate required fields
    validation = validate_required_fields(data, ['email', 'password', 'name'])
    if not validation['valid']:
        return jsonify({"error": validation['message']}), 400
    
    # Validate email
    if not validate_email(data['email']):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate password
    password_validation = validate_password(data['password'])
    if not password_validation['valid']:
        return jsonify({"error": password_validation['message']}), 400
    
    # Check if user already exists
    if auth_service.get_user_by_email(data['email']):
        return jsonify({"error": "Email already registered"}), 409
    
    # Create user
    user = auth_service.create_user(
        email=data['email'],
        password=data['password'],
        name=data['name']
    )
    
    # Generate access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Returns:
        Response: JSON response
    """
    data = request.get_json()
    
    # Validate required fields
    validation = validate_required_fields(data, ['email', 'password'])
    if not validation['valid']:
        return jsonify({"error": validation['message']}), 400
    
    # Authenticate user
    user = auth_service.authenticate_user(
        email=data['email'],
        password=data['password']
    )
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Generate access token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Get current user
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get user
    user = auth_service.get_user_by_id(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    }), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """
    Change user password
    
    Returns:
        Response: JSON response
    """
    data = request.get_json()
    
    # Validate required fields
    validation = validate_required_fields(data, ['current_password', 'new_password'])
    if not validation['valid']:
        return jsonify({"error": validation['message']}), 400
    
    # Validate new password
    password_validation = validate_password(data['new_password'])
    if not password_validation['valid']:
        return jsonify({"error": password_validation['message']}), 400
    
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Change password
    success = auth_service.change_password(
        user_id=user_id,
        current_password=data['current_password'],
        new_password=data['new_password']
    )
    
    if not success:
        return jsonify({"error": "Current password is incorrect"}), 401
    
    return jsonify({
        "message": "Password changed successfully"
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user
    
    Returns:
        Response: JSON response
    """
    # Note: JWT tokens are stateless, so we can't invalidate them
    # In a real application, you would use a token blacklist
    
    return jsonify({
        "message": "Logout successful"
    }), 200
