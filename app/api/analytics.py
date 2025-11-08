"""
AdGenius AI Backend - Analytics API
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.analytics_service_simple import AnalyticsService

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# Create analytics service
analytics_service = AnalyticsService()

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """
    Get analytics dashboard data
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    platform = request.args.get('platform')
    
    # Get dashboard data
    dashboard_data = analytics_service.get_dashboard_data(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        platform=platform
    )
    
    return jsonify(dashboard_data), 200

@analytics_bp.route('/campaigns/<campaign_id>', methods=['GET'])
@jwt_required()
def get_campaign_analytics(campaign_id):
    """
    Get analytics for a specific campaign
    
    Args:
        campaign_id (str): Campaign ID
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    metrics = request.args.get('metrics', 'impressions,clicks,conversions,spend')
    
    # Parse metrics
    metrics_list = metrics.split(',') if metrics else []
    
    # Get campaign analytics
    analytics_data = analytics_service.get_campaign_analytics(
        user_id=user_id,
        campaign_id=campaign_id,
        start_date=start_date,
        end_date=end_date,
        metrics=metrics_list
    )
    
    if 'error' in analytics_data:
        return jsonify({"error": analytics_data['error']}), 404
    
    return jsonify(analytics_data), 200

@analytics_bp.route('/platforms/<platform>', methods=['GET'])
@jwt_required()
def get_platform_analytics(platform):
    """
    Get analytics for a specific platform
    
    Args:
        platform (str): Platform name (facebook, instagram, tiktok, shopee)
        
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    metrics = request.args.get('metrics', 'impressions,clicks,conversions,spend')
    
    # Parse metrics
    metrics_list = metrics.split(',') if metrics else []
    
    # Get platform analytics
    analytics_data = analytics_service.get_platform_analytics(
        user_id=user_id,
        platform=platform,
        start_date=start_date,
        end_date=end_date,
        metrics=metrics_list
    )
    
    if 'error' in analytics_data:
        return jsonify({"error": analytics_data['error']}), 404
    
    return jsonify(analytics_data), 200

@analytics_bp.route('/audience', methods=['GET'])
@jwt_required()
def get_audience_insights():
    """
    Get audience insights
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    platform = request.args.get('platform')
    campaign_id = request.args.get('campaign_id')
    
    # Get audience insights
    insights = analytics_service.get_audience_insights(
        user_id=user_id,
        platform=platform,
        campaign_id=campaign_id
    )
    
    return jsonify(insights), 200

@analytics_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_performance_metrics():
    """
    Get performance metrics
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    platform = request.args.get('platform')
    campaign_id = request.args.get('campaign_id')
    group_by = request.args.get('group_by', 'day')  # day, week, month
    
    # Get performance metrics
    metrics = analytics_service.get_performance_metrics(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        platform=platform,
        campaign_id=campaign_id,
        group_by=group_by
    )
    
    return jsonify(metrics), 200

@analytics_bp.route('/roi', methods=['GET'])
@jwt_required()
def get_roi_analysis():
    """
    Get ROI analysis
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    platform = request.args.get('platform')
    campaign_id = request.args.get('campaign_id')
    
    # Get ROI analysis
    analysis = analytics_service.get_roi_analysis(
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        platform=platform,
        campaign_id=campaign_id
    )
    
    return jsonify(analysis), 200

@analytics_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """
    Get AI-powered recommendations
    
    Returns:
        Response: JSON response
    """
    # Get user ID from JWT
    user_id = get_jwt_identity()
    
    # Get query parameters
    platform = request.args.get('platform')
    campaign_id = request.args.get('campaign_id')
    
    # Get recommendations
    recommendations = analytics_service.get_recommendations(
        user_id=user_id,
        platform=platform,
        campaign_id=campaign_id
    )
    
    return jsonify(recommendations), 200
