"""
AdGenius AI Backend - Campaigns API
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.campaign_service import CampaignService
from app.utils.validators import validate_required_fields

# Create blueprint
campaigns_bp = Blueprint('campaigns', __name__, url_prefix='/campaigns')

# Create campaign service
campaign_service = CampaignService()

@campaigns_bp.route('/', methods=['GET'])
@jwt_required()
def get_campaigns():
    """
    Get all campaigns for current user
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    platform = request.args.get('platform')
    status = request.args.get('status')
    
    # Get campaigns
    result = campaign_service.get_campaigns(
        user_id=user_id,
        page=page,
        per_page=per_page,
        platform=platform,
        status=status
    )
    
    return jsonify(result), 200

@campaigns_bp.route('/<campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign(campaign_id):
    """
    Get campaign by ID
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get campaign
    campaign = campaign_service.get_campaign_by_id(
        campaign_id=campaign_id,
        user_id=user_id
    )
    
    if not campaign:
        return jsonify({"error": "Campaign not found"}), 404
    
    return jsonify({
        "campaign": campaign
    }), 200

@campaigns_bp.route('/', methods=['POST'])
@jwt_required()
def create_campaign():
    """
    Create a new campaign
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Validate required fields
    validation = validate_required_fields(data, ['name', 'platform', 'objective'])
    if not validation['valid']:
        return jsonify({"error": validation['message']}), 400
    
    # Create campaign
    campaign = campaign_service.create_campaign(
        user_id=user_id,
        name=data['name'],
        platform=data['platform'],
        objective=data['objective'],
        budget=data.get('budget'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        targeting=data.get('targeting', {}),
        creatives=data.get('creatives', [])
    )
    
    return jsonify({
        "message": "Campaign created successfully",
        "campaign": campaign
    }), 201

@campaigns_bp.route('/<campaign_id>', methods=['PUT'])
@jwt_required()
def update_campaign(campaign_id):
    """
    Update campaign
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json()
    
    # Update campaign
    campaign = campaign_service.update_campaign(
        campaign_id=campaign_id,
        user_id=user_id,
        **data
    )
    
    if not campaign:
        return jsonify({"error": "Campaign not found"}), 404
    
    return jsonify({
        "message": "Campaign updated successfully",
        "campaign": campaign
    }), 200

@campaigns_bp.route('/<campaign_id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(campaign_id):
    """
    Delete campaign
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Delete campaign
    success = campaign_service.delete_campaign(
        campaign_id=campaign_id,
        user_id=user_id
    )
    
    if not success:
        return jsonify({"error": "Campaign not found"}), 404
    
    return jsonify({
        "message": "Campaign deleted successfully"
    }), 200

@campaigns_bp.route('/<campaign_id>/publish', methods=['POST'])
@jwt_required()
def publish_campaign(campaign_id):
    """
    Publish campaign to platform
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Publish campaign
    result = campaign_service.publish_campaign(
        campaign_id=campaign_id,
        user_id=user_id
    )
    
    if 'error' in result:
        return jsonify({"error": result['error']}), 400
    
    return jsonify({
        "message": "Campaign published successfully",
        "platform_id": result.get('platform_id'),
        "status": result.get('status')
    }), 200

@campaigns_bp.route('/<campaign_id>/pause', methods=['POST'])
@jwt_required()
def pause_campaign(campaign_id):
    """
    Pause campaign
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Pause campaign
    success = campaign_service.pause_campaign(
        campaign_id=campaign_id,
        user_id=user_id
    )
    
    if not success:
        return jsonify({"error": "Campaign not found or cannot be paused"}), 404
    
    return jsonify({
        "message": "Campaign paused successfully"
    }), 200

@campaigns_bp.route('/<campaign_id>/resume', methods=['POST'])
@jwt_required()
def resume_campaign(campaign_id):
    """
    Resume campaign
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Resume campaign
    success = campaign_service.resume_campaign(
        campaign_id=campaign_id,
        user_id=user_id
    )
    
    if not success:
        return jsonify({"error": "Campaign not found or cannot be resumed"}), 404
    
    return jsonify({
        "message": "Campaign resumed successfully"
    }), 200

@campaigns_bp.route('/<campaign_id>/optimize', methods=['POST'])
@jwt_required()
def optimize_campaign(campaign_id):
    """
    Optimize campaign using AI
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get request data
    data = request.get_json() or {}
    
    # Optimize campaign
    result = campaign_service.optimize_campaign(
        campaign_id=campaign_id,
        user_id=user_id,
        optimization_type=data.get('optimization_type', 'auto')
    )
    
    if 'error' in result:
        return jsonify({"error": result['error']}), 400
    
    return jsonify({
        "message": "Campaign optimization started",
        "recommendations": result.get('recommendations', [])
    }), 200
