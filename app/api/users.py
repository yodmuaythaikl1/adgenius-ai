"""
AdGenius AI Backend - Users API
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.user_service import UserService
from app.utils.validators import validate_email, validate_required_fields

# Create blueprint
users_bp = Blueprint('users', __name__, url_prefix='/users')

# Create user service
user_service = UserService()

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get user profile
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get user profile
    profile = user_service.get_user_profile(user_id)
    
    if not profile:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "profile": profile
    }), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Update user profile
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Update user profile
    profile = user_service.update_user_profile(
        user_id=user_id,
        **data
    )
    
    if not profile:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "message": "Profile updated successfully",
        "profile": profile
    }), 200

@users_bp.route('/platform-accounts', methods=['GET'])
@jwt_required()
def get_platform_accounts():
    """
    Get user's platform accounts
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get platform accounts
    accounts = user_service.get_platform_accounts(user_id)
    
    return jsonify({
        "accounts": accounts
    }), 200

@users_bp.route('/platform-accounts', methods=['POST'])
@jwt_required()
def add_platform_account():
    """
    Add platform account
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Validate required fields
    validation = validate_required_fields(data, ['platform', 'credentials'])
    if not validation['valid']:
        return jsonify({"error": validation['message']}), 400
    
    # Add platform account
    account = user_service.add_platform_account(
        user_id=user_id,
        platform=data['platform'],
        credentials=data['credentials']
    )
    
    if 'error' in account:
        return jsonify({"error": account['error']}), 400
    
    return jsonify({
        "message": "Platform account added successfully",
        "account": account
    }), 201

@users_bp.route('/platform-accounts/<account_id>', methods=['PUT'])
@jwt_required()
def update_platform_account(account_id):
    """
    Update platform account
    
    Args:
        account_id (str): Account ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Update platform account
    account = user_service.update_platform_account(
        user_id=user_id,
        account_id=account_id,
        **data
    )
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    if 'error' in account:
        return jsonify({"error": account['error']}), 400
    
    return jsonify({
        "message": "Platform account updated successfully",
        "account": account
    }), 200

@users_bp.route('/platform-accounts/<account_id>', methods=['DELETE'])
@jwt_required()
def delete_platform_account(account_id):
    """
    Delete platform account
    
    Args:
        account_id (str): Account ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Delete platform account
    success = user_service.delete_platform_account(
        user_id=user_id,
        account_id=account_id
    )
    
    if not success:
        return jsonify({"error": "Account not found"}), 404
    
    return jsonify({
        "message": "Platform account deleted successfully"
    }), 200

@users_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """
    Get user settings
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get user settings
    settings = user_service.get_user_settings(user_id)
    
    return jsonify({
        "settings": settings
    }), 200

@users_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """
    Update user settings
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Update user settings
    settings = user_service.update_user_settings(
        user_id=user_id,
        **data
    )
    
    return jsonify({
        "message": "Settings updated successfully",
        "settings": settings
    }), 200

@users_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """
    Get user notifications
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    read = request.args.get('read')
    
    # Convert read parameter to boolean if provided
    if read is not None:
        read = read.lower() == 'true'
    
    # Get notifications
    result = user_service.get_notifications(
        user_id=user_id,
        page=page,
        per_page=per_page,
        read=read
    )
    
    return jsonify(result), 200

@users_bp.route('/notifications/<notification_id>/read', methods=['POST'])
@jwt_required()
def mark_notification_as_read(notification_id):
    """
    Mark notification as read
    
    Args:
        notification_id (str): Notification ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Mark notification as read
    success = user_service.mark_notification_as_read(
        user_id=user_id,
        notification_id=notification_id
    )
    
    if not success:
        return jsonify({"error": "Notification not found"}), 404
    
    return jsonify({
        "message": "Notification marked as read"
    }), 200
