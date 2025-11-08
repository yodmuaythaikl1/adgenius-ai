"""
AdGenius AI Backend - Analytics Service
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from app.models.user import User
from app.models.campaign import Campaign
from app.models.analytics import (
    CampaignAnalytics, UserAnalytics, DailyMetric, 
    AudienceInsight, CreativePerformance, Recommendation
)
from app.platform_connectors.facebook_connector import FacebookConnector
from app.platform_connectors.instagram_connector import InstagramConnector
from app.platform_connectors.tiktok_connector import TikTokConnector
from app.platform_connectors.shopee_connector import ShopeeConnector
from app.ai_modules.campaign_optimization import CampaignOptimizationAI

class AnalyticsService:
    """Analytics service"""
    
    def __init__(self):
        """Initialize analytics service"""
        self.facebook_connector = FacebookConnector()
        self.instagram_connector = InstagramConnector()
        self.tiktok_connector = TikTokConnector()
        self.shopee_connector = ShopeeConnector()
        self.optimization_ai = CampaignOptimizationAI()
    
    def get_dashboard_data(self, user_id: str, start_date: Optional[str] = None, 
                          end_date: Optional[str] = None, platform: Optional[str] = None) -> Dict:
        """
        Get analytics dashboard data
        
        Args:
            user_id (str): User ID
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            platform (Optional[str], optional): Platform. Defaults to None.
            
        Returns:
            Dict: Dashboard data
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Set default date range if not provided (last 30 days)
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date)
        
        if not start_date:
            start_date_obj = end_date_obj - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date)
        
        # Create query for campaigns
        campaign_query = {'user': user}
        
        if platform:
            campaign_query['platform'] = platform
        
        # Get campaigns
        campaigns = Campaign.objects(**campaign_query)
        
        # Get campaign IDs
        campaign_ids = [str(campaign.id) for campaign in campaigns]
        
        # Create query for analytics
        analytics_query = {
            'user': user,
            'start_date__lte': end_date_obj,
            'end_date__gte': start_date_obj if 'end_date' in CampaignAnalytics._fields else None
        }
        
        if campaign_ids:
            analytics_query['campaign__in'] = campaign_ids
        
        if platform:
            analytics_query['platform'] = platform
        
        # Get analytics
        analytics_list = CampaignAnalytics.objects(**analytics_query)
        
        # Calculate totals
        total_impressions = sum(analytics.total_impressions for analytics in analytics_list)
        total_clicks = sum(analytics.total_clicks for analytics in analytics_list)
        total_conversions = sum(analytics.total_conversions for analytics in analytics_list)
        total_spend = sum(analytics.total_spend for analytics in analytics_list)
        total_revenue = sum(analytics.total_revenue for analytics in analytics_list)
        
        # Calculate averages
        average_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        average_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        average_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
        average_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        average_cost_per_conversion = (total_spend / total_conversions) if total_conversions > 0 else 0
        roas = (total_revenue / total_spend) if total_spend > 0 else 0
        
        # Get daily metrics
        daily_metrics = self._get_daily_metrics(analytics_list, start_date_obj, end_date_obj)
        
        # Get platform breakdown
        platform_breakdown = self._get_platform_breakdown(analytics_list)
        
        # Get campaign breakdown
        campaign_breakdown = self._get_campaign_breakdown(analytics_list)
        
        # Get recommendations
        recommendations = self._get_recommendations(analytics_list)
        
        return {
            'summary': {
                'total_campaigns': len(campaign_ids),
                'active_campaigns': Campaign.objects(user=user, status='active').count(),
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'total_spend': total_spend,
                'total_revenue': total_revenue,
                'average_ctr': average_ctr,
                'average_cpc': average_cpc,
                'average_cpm': average_cpm,
                'average_conversion_rate': average_conversion_rate,
                'average_cost_per_conversion': average_cost_per_conversion,
                'roas': roas
            },
            'daily_metrics': daily_metrics,
            'platform_breakdown': platform_breakdown,
            'campaign_breakdown': campaign_breakdown,
            'recommendations': recommendations
        }
    
    def get_campaign_analytics(self, user_id: str, campaign_id: str, 
                              start_date: Optional[str] = None, end_date: Optional[str] = None, 
                              metrics: Optional[List[str]] = None) -> Dict:
        """
        Get analytics for a specific campaign
        
        Args:
            user_id (str): User ID
            campaign_id (str): Campaign ID
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            metrics (Optional[List[str]], optional): Metrics to include. Defaults to None.
            
        Returns:
            Dict: Campaign analytics
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user).first()
        
        if not campaign:
            return {'error': 'Campaign not found'}
        
        # Set default date range if not provided (last 30 days)
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date)
        
        if not start_date:
            start_date_obj = end_date_obj - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date)
        
        # Find analytics
        analytics = CampaignAnalytics.objects(
            user=user,
            campaign=campaign,
            start_date__lte=end_date_obj,
            end_date__gte=start_date_obj if 'end_date' in CampaignAnalytics._fields else None
        ).first()
        
        if not analytics:
            # If no analytics found, fetch from platform
            connector = self._get_platform_connector(campaign.platform)
            
            if not connector:
                return {'error': f'Platform {campaign.platform} is not supported'}
            
            # Fetch analytics from platform
            platform_analytics = connector.get_campaign_analytics(
                campaign_id=campaign.platform_campaign_id,
                start_date=start_date_obj,
                end_date=end_date_obj
            )
            
            if 'error' in platform_analytics:
                return platform_analytics
            
            # Create analytics object
            analytics = self._create_campaign_analytics(
                user=user,
                campaign=campaign,
                platform=campaign.platform,
                start_date=start_date_obj,
                end_date=end_date_obj,
                data=platform_analytics
            )
        
        # Filter metrics if provided
        result = analytics.to_dict()
        
        if metrics:
            result = {k: v for k, v in result.items() if k in metrics or k in ['id', 'campaign_id', 'user_id']}
        
        # Add daily metrics
        result['daily_metrics'] = analytics.get_daily_metrics()
        
        # Add audience insights
        result['audience_insights'] = analytics.get_audience_insights()
        
        # Add creative performance
        result['creative_performance'] = analytics.get_creative_performance()
        
        # Add recommendations
        result['recommendations'] = analytics.get_recommendations()
        
        return result
    
    def get_platform_analytics(self, user_id: str, platform: str, 
                              start_date: Optional[str] = None, end_date: Optional[str] = None, 
                              metrics: Optional[List[str]] = None) -> Dict:
        """
        Get analytics for a specific platform
        
        Args:
            user_id (str): User ID
            platform (str): Platform name
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            metrics (Optional[List[str]], optional): Metrics to include. Defaults to None.
            
        Returns:
            Dict: Platform analytics
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Set default date range if not provided (last 30 days)
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date)
        
        if not start_date:
            start_date_obj = end_date_obj - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date)
        
        # Find analytics
        analytics_list = CampaignAnalytics.objects(
            user=user,
            platform=platform,
            start_date__lte=end_date_obj,
            end_date__gte=start_date_obj if 'end_date' in CampaignAnalytics._fields else None
        )
        
        if not analytics_list:
            # If no analytics found, fetch from platform
            connector = self._get_platform_connector(platform)
            
            if not connector:
                return {'error': f'Platform {platform} is not supported'}
            
            # Get campaigns for platform
            campaigns = Campaign.objects(user=user, platform=platform)
            
            if not campaigns:
                return {'error': f'No campaigns found for platform {platform}'}
            
            # Fetch analytics for each campaign
            analytics_list = []
            
            for campaign in campaigns:
                if not campaign.platform_campaign_id:
                    continue
                
                # Fetch analytics from platform
                platform_analytics = connector.get_campaign_analytics(
                    campaign_id=campaign.platform_campaign_id,
                    start_date=start_date_obj,
                    end_date=end_date_obj
                )
                
                if 'error' in platform_analytics:
                    continue
                
                # Create analytics object
                analytics = self._create_campaign_analytics(
                    user=user,
                    campaign=campaign,
                    platform=platform,
                    start_date=start_date_obj,
                    end_date=end_date_obj,
                    data=platform_analytics
                )
                
                analytics_list.append(analytics)
        
        # Calculate totals
        total_impressions = sum(analytics.total_impressions for analytics in analytics_list)
        total_clicks = sum(analytics.total_clicks for analytics in analytics_list)
        total_conversions = sum(analytics.total_conversions for analytics in analytics_list)
        total_spend = sum(analytics.total_spend for analytics in analytics_list)
        total_revenue = sum(analytics.total_revenue for analytics in analytics_list)
        
        # Calculate averages
        average_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        average_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        average_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
        average_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        average_cost_per_conversion = (total_spend / total_conversions) if total_conversions > 0 else 0
        roas = (total_revenue / total_spend) if total_spend > 0 else 0
        
        # Get daily metrics
        daily_metrics = self._get_daily_metrics(analytics_list, start_date_obj, end_date_obj)
        
        # Get campaign breakdown
        campaign_breakdown = self._get_campaign_breakdown(analytics_list)
        
        # Filter metrics if provided
        result = {
            'platform': platform,
            'start_date': start_date_obj.isoformat(),
            'end_date': end_date_obj.isoformat(),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_spend': total_spend,
            'total_revenue': total_revenue,
            'average_ctr': average_ctr,
            'average_cpc': average_cpc,
            'average_cpm': average_cpm,
            'average_conversion_rate': average_conversion_rate,
            'average_cost_per_conversion': average_cost_per_conversion,
            'roas': roas,
            'daily_metrics': daily_metrics,
            'campaign_breakdown': campaign_breakdown
        }
        
        if metrics:
            result = {k: v for k, v in result.items() if k in metrics or k in ['platform', 'start_date', 'end_date']}
        
        return result
    
    def get_audience_insights(self, user_id: str, platform: Optional[str] = None, 
                             campaign_id: Optional[str] = None) -> Dict:
        """
        Get audience insights
        
        Args:
            user_id (str): User ID
            platform (Optional[str], optional): Platform. Defaults to None.
            campaign_id (Optional[str], optional): Campaign ID. Defaults to None.
            
        Returns:
            Dict: Audience insights
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Create query
        query = {'user': user}
        
        if platform:
            query['platform'] = platform
        
        if campaign_id:
            campaign = Campaign.objects(id=campaign_id, user=user).first()
            
            if not campaign:
                return {'error': 'Campaign not found'}
            
            query['campaign'] = campaign
        
        # Find analytics
        analytics_list = CampaignAnalytics.objects(**query)
        
        if not analytics_list:
            return {'error': 'No analytics data found'}
        
        # Combine audience insights
        combined_insights = {
            'age_gender': {},
            'locations': {},
            'interests': {},
            'behaviors': {},
            'devices': {},
            'platforms': {},
            'placements': {},
            'time_of_day': {},
            'day_of_week': {}
        }
        
        for analytics in analytics_list:
            if not analytics.audience_insights:
                continue
            
            insights = analytics.get_audience_insights()
            
            # Combine age_gender
            for age_gender, value in insights.get('age_gender', {}).items():
                if age_gender in combined_insights['age_gender']:
                    combined_insights['age_gender'][age_gender] += value
                else:
                    combined_insights['age_gender'][age_gender] = value
            
            # Combine locations
            for location, value in insights.get('locations', {}).items():
                if location in combined_insights['locations']:
                    combined_insights['locations'][location] += value
                else:
                    combined_insights['locations'][location] = value
            
            # Combine interests
            for interest, value in insights.get('interests', {}).items():
                if interest in combined_insights['interests']:
                    combined_insights['interests'][interest] += value
                else:
                    combined_insights['interests'][interest] = value
            
            # Combine behaviors
            for behavior, value in insights.get('behaviors', {}).items():
                if behavior in combined_insights['behaviors']:
                    combined_insights['behaviors'][behavior] += value
                else:
                    combined_insights['behaviors'][behavior] = value
            
            # Combine devices
            for device, value in insights.get('devices', {}).items():
                if device in combined_insights['devices']:
                    combined_insights['devices'][device] += value
                else:
                    combined_insights['devices'][device] = value
            
            # Combine platforms
            for platform_name, value in insights.get('platforms', {}).items():
                if platform_name in combined_insights['platforms']:
                    combined_insights['platforms'][platform_name] += value
                else:
                    combined_insights['platforms'][platform_name] = value
            
            # Combine placements
            for placement, value in insights.get('placements', {}).items():
                if placement in combined_insights['placements']:
                    combined_insights['placements'][placement] += value
                else:
                    combined_insights['placements'][placement] = value
            
            # Combine time_of_day
            for time, value in insights.get('time_of_day', {}).items():
                if time in combined_insights['time_of_day']:
                    combined_insights['time_of_day'][time] += value
                else:
                    combined_insights['time_of_day'][time] = value
            
            # Combine day_of_week
            for day, value in insights.get('day_of_week', {}).items():
                if day in combined_insights['day_of_week']:
                    combined_insights['day_of_week'][day] += value
                else:
                    combined_insights['day_of_week'][day] = value
        
        return combined_insights
    
    def get_performance_metrics(self, user_id: str, start_date: Optional[str] = None, 
                               end_date: Optional[str] = None, platform: Optional[str] = None, 
                               campaign_id: Optional[str] = None, group_by: str = 'day') -> Dict:
        """
        Get performance metrics
        
        Args:
            user_id (str): User ID
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            platform (Optional[str], optional): Platform. Defaults to None.
            campaign_id (Optional[str], optional): Campaign ID. Defaults to None.
            group_by (str, optional): Group by (day, week, month). Defaults to 'day'.
            
        Returns:
            Dict: Performance metrics
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Set default date range if not provided (last 30 days)
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date)
        
        if not start_date:
            start_date_obj = end_date_obj - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date)
        
        # Create query
        query = {
            'user': user,
            'start_date__lte': end_date_obj,
            'end_date__gte': start_date_obj if 'end_date' in CampaignAnalytics._fields else None
        }
        
        if platform:
            query['platform'] = platform
        
        if campaign_id:
            campaign = Campaign.objects(id=campaign_id, user=user).first()
            
            if not campaign:
                return {'error': 'Campaign not found'}
            
            query['campaign'] = campaign
        
        # Find analytics
        analytics_list = CampaignAnalytics.objects(**query)
        
        if not analytics_list:
            return {'error': 'No analytics data found'}
        
        # Get daily metrics
        daily_metrics = self._get_daily_metrics(analytics_list, start_date_obj, end_date_obj)
        
        # Group metrics
        if group_by == 'day':
            grouped_metrics = daily_metrics
        else:
            grouped_metrics = self._group_metrics(daily_metrics, group_by)
        
        return {
            'metrics': grouped_metrics
        }
    
    def get_roi_analysis(self, user_id: str, start_date: Optional[str] = None, 
                        end_date: Optional[str] = None, platform: Optional[str] = None, 
                        campaign_id: Optional[str] = None) -> Dict:
        """
        Get ROI analysis
        
        Args:
            user_id (str): User ID
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            platform (Optional[str], optional): Platform. Defaults to None.
            campaign_id (Optional[str], optional): Campaign ID. Defaults to None.
            
        Returns:
            Dict: ROI analysis
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Set default date range if not provided (last 30 days)
        if not end_date:
            end_date_obj = datetime.utcnow()
        else:
            end_date_obj = datetime.fromisoformat(end_date)
        
        if not start_date:
            start_date_obj = end_date_obj - timedelta(days=30)
        else:
            start_date_obj = datetime.fromisoformat(start_date)
        
        # Create query
        query = {
            'user': user,
            'start_date__lte': end_date_obj,
            'end_date__gte': start_date_obj if 'end_date' in CampaignAnalytics._fields else None
        }
        
        if platform:
            query['platform'] = platform
        
        if campaign_id:
            campaign = Campaign.objects(id=campaign_id, user=user).first()
            
            if not campaign:
                return {'error': 'Campaign not found'}
            
            query['campaign'] = campaign
        
        # Find analytics
        analytics_list = CampaignAnalytics.objects(**query)
        
        if not analytics_list:
            return {'error': 'No analytics data found'}
        
        # Calculate ROI metrics
        total_spend = sum(analytics.total_spend for analytics in analytics_list)
        total_revenue = sum(analytics.total_revenue for analytics in analytics_list)
        total_conversions = sum(analytics.total_conversions for analytics in analytics_list)
        
        # Calculate ROI
        roi = ((total_revenue - total_spend) / total_spend * 100) if total_spend > 0 else 0
        
        # Calculate ROAS
        roas = (total_revenue / total_spend) if total_spend > 0 else 0
        
        # Calculate cost per conversion
        cost_per_conversion = (total_spend / total_conversions) if total_conversions > 0 else 0
        
        # Get daily ROI metrics
        daily_metrics = self._get_daily_metrics(analytics_list, start_date_obj, end_date_obj)
        
        # Calculate daily ROI
        daily_roi = []
        
        for metric in daily_metrics:
            spend = metric.get('spend', 0)
            revenue = metric.get('revenue', 0)
            
            daily_roi_value = ((revenue - spend) / spend * 100) if spend > 0 else 0
            
            daily_roi.append({
                'date': metric.get('date'),
                'roi': daily_roi_value,
                'roas': (revenue / spend) if spend > 0 else 0,
                'spend': spend,
                'revenue': revenue
            })
        
        # Get platform breakdown
        platform_breakdown = {}
        
        for analytics in analytics_list:
            platform_name = analytics.platform
            
            if platform_name not in platform_breakdown:
                platform_breakdown[platform_name] = {
                    'spend': 0,
                    'revenue': 0,
                    'roi': 0,
                    'roas': 0
                }
            
            platform_breakdown[platform_name]['spend'] += analytics.total_spend
            platform_breakdown[platform_name]['revenue'] += analytics.total_revenue
        
        # Calculate ROI and ROAS for each platform
        for platform_name, data in platform_breakdown.items():
            spend = data['spend']
            revenue = data['revenue']
            
            data['roi'] = ((revenue - spend) / spend * 100) if spend > 0 else 0
            data['roas'] = (revenue / spend) if spend > 0 else 0
        
        # Get campaign breakdown
        campaign_breakdown = {}
        
        for analytics in analytics_list:
            campaign_name = analytics.campaign.name
            
            if campaign_name not in campaign_breakdown:
                campaign_breakdown[campaign_name] = {
                    'spend': 0,
                    'revenue': 0,
                    'roi': 0,
                    'roas': 0
                }
            
            campaign_breakdown[campaign_name]['spend'] += analytics.total_spend
            campaign_breakdown[campaign_name]['revenue'] += analytics.total_revenue
        
        # Calculate ROI and ROAS for each campaign
        for campaign_name, data in campaign_breakdown.items():
            spend = data['spend']
            revenue = data['revenue']
            
            data['roi'] = ((revenue - spend) / spend * 100) if spend > 0 else 0
            data['roas'] = (revenue / spend) if spend > 0 else 0
        
        return {
            'summary': {
                'total_spend': total_spend,
                'total_revenue': total_revenue,
                'roi': roi,
                'roas': roas,
                'cost_per_conversion': cost_per_conversion
            },
            'daily_roi': daily_roi,
            'platform_breakdown': platform_breakdown,
            'campaign_breakdown': campaign_breakdown
        }
    
    def get_recommendations(self, user_id: str, platform: Optional[str] = None, 
                           campaign_id: Optional[str] = None) -> Dict:
        """
        Get AI-powered recommendations
        
        Args:
            user_id (str): User ID
            platform (Optional[str], optional): Platform. Defaults to None.
            campaign_id (Optional[str], optional): Campaign ID. Defaults to None.
            
        Returns:
            Dict: Recommendations
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Create query
        query = {'user': user}
        
        if platform:
            query['platform'] = platform
        
        if campaign_id:
            campaign = Campaign.objects(id=campaign_id, user=user).first()
            
            if not campaign:
                return {'error': 'Campaign not found'}
            
            query['campaign'] = campaign
        
        # Find analytics
        analytics_list = CampaignAnalytics.objects(**query)
        
        if not analytics_list:
            return {'error': 'No analytics data found'}
        
        # Get recommendations
        recommendations = []
        
        for analytics in analytics_list:
            recommendations.extend(analytics.get_recommendations())
        
        # If no recommendations found, generate new ones
        if not recommendations and campaign_id:
            campaign = Campaign.objects(id=campaign_id, user=user).first()
            
            if campaign:
                # Generate recommendations
                result = self.optimization_ai.optimize_campaign(campaign, 'auto')
                
                if 'recommendations' in result:
                    recommendations = result['recommendations']
        
        return {
            'recommendations': recommendations
        }
    
    def _get_daily_metrics(self, analytics_list: List[CampaignAnalytics], 
                          start_date: datetime, end_date: datetime) -> List[Dict]:
        """
        Get daily metrics from analytics list
        
        Args:
            analytics_list (List[CampaignAnalytics]): Analytics list
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            List[Dict]: Daily metrics
        """
        # Create date range
        date_range = []
        current_date = start_date
        
        while current_date <= end_date:
            date_range.append(current_date.date())
            current_date += timedelta(days=1)
        
        # Initialize daily metrics
        daily_metrics = {date.isoformat(): {
            'date': date.isoformat(),
            'impressions': 0,
            'clicks': 0,
            'conversions': 0,
            'spend': 0.0,
            'revenue': 0.0,
            'ctr': 0.0,
            'cpc': 0.0,
            'cpm': 0.0,
            'conversion_rate': 0.0,
            'cost_per_conversion': 0.0,
            'roas': 0.0
        } for date in date_range}
        
        # Aggregate daily metrics
        for analytics in analytics_list:
            for metric in analytics.daily_metrics:
                date_str = metric.date.date().isoformat()
                
                if date_str in daily_metrics:
                    daily_metrics[date_str]['impressions'] += metric.impressions
                    daily_metrics[date_str]['clicks'] += metric.clicks
                    daily_metrics[date_str]['conversions'] += metric.conversions
                    daily_metrics[date_str]['spend'] += metric.spend
                    daily_metrics[date_str]['revenue'] += metric.revenue
        
        # Calculate derived metrics
        for date_str, metric in daily_metrics.items():
            impressions = metric['impressions']
            clicks = metric['clicks']
            conversions = metric['conversions']
            spend = metric['spend']
            revenue = metric['revenue']
            
            # Calculate CTR
            if impressions > 0:
                metric['ctr'] = (clicks / impressions) * 100
            
            # Calculate CPC
            if clicks > 0:
                metric['cpc'] = spend / clicks
            
            # Calculate CPM
            if impressions > 0:
                metric['cpm'] = (spend / impressions) * 1000
            
            # Calculate conversion rate
            if clicks > 0:
                metric['conversion_rate'] = (conversions / clicks) * 100
            
            # Calculate cost per conversion
            if conversions > 0:
                metric['cost_per_conversion'] = spend / conversions
            
            # Calculate ROAS
            if spend > 0:
                metric['roas'] = revenue / spend
        
        return list(daily_metrics.values())
    
    def _group_metrics(self, daily_metrics: List[Dict], group_by: str) -> List[Dict]:
        """
        Group metrics by week or month
        
        Args:
            daily_metrics (List[Dict]): Daily metrics
            group_by (str): Group by (week, month)
            
        Returns:
            List[Dict]: Grouped metrics
        """
        grouped_metrics = {}
        
        for metric in daily_metrics:
            date = datetime.fromisoformat(metric['date'])
            
            if group_by == 'week':
                # Group by week (Monday as first day)
                week_start = date - timedelta(days=date.weekday())
                group_key = week_start.date().isoformat()
                group_label = f"Week of {week_start.strftime('%b %d, %Y')}"
            else:  # month
                # Group by month
                group_key = date.strftime('%Y-%m')
                group_label = date.strftime('%b %Y')
            
            if group_key not in grouped_metrics:
                grouped_metrics[group_key] = {
                    'period': group_label,
                    'impressions': 0,
                    'clicks': 0,
                    'conversions': 0,
                    'spend': 0.0,
                    'revenue': 0.0,
                    'ctr': 0.0,
                    'cpc': 0.0,
                    'cpm': 0.0,
                    'conversion_rate': 0.0,
                    'cost_per_conversion': 0.0,
                    'roas': 0.0
                }
            
            grouped_metrics[group_key]['impressions'] += metric['impressions']
            grouped_metrics[group_key]['clicks'] += metric['clicks']
            grouped_metrics[group_key]['conversions'] += metric['conversions']
            grouped_metrics[group_key]['spend'] += metric['spend']
            grouped_metrics[group_key]['revenue'] += metric['revenue']
        
        # Calculate derived metrics for each group
        for group_key, group_data in grouped_metrics.items():
            impressions = group_data['impressions']
            clicks = group_data['clicks']
            conversions = group_data['conversions']
            spend = group_data['spend']
            revenue = group_data['revenue']
            
            # Calculate CTR
            if impressions > 0:
                group_data['ctr'] = (clicks / impressions) * 100
            
            # Calculate CPC
            if clicks > 0:
                group_data['cpc'] = spend / clicks
            
            # Calculate CPM
            if impressions > 0:
                group_data['cpm'] = (spend / impressions) * 1000
            
            # Calculate conversion rate
            if clicks > 0:
                group_data['conversion_rate'] = (conversions / clicks) * 100
            
            # Calculate cost per conversion
            if conversions > 0:
                group_data['cost_per_conversion'] = spend / conversions
            
            # Calculate ROAS
            if spend > 0:
                group_data['roas'] = revenue / spend
        
        return list(grouped_metrics.values())
    
    def _get_platform_breakdown(self, analytics_list: List[CampaignAnalytics]) -> Dict:
        """
        Get platform breakdown from analytics list
        
        Args:
            analytics_list (List[CampaignAnalytics]): Analytics list
            
        Returns:
            Dict: Platform breakdown
        """
        platform_breakdown = {}
        
        for analytics in analytics_list:
            platform = analytics.platform
            
            if platform not in platform_breakdown:
                platform_breakdown[platform] = {
                    'impressions': 0,
                    'clicks': 0,
                    'conversions': 0,
                    'spend': 0.0,
                    'revenue': 0.0,
                    'ctr': 0.0,
                    'cpc': 0.0,
                    'cpm': 0.0,
                    'conversion_rate': 0.0,
                    'cost_per_conversion': 0.0,
                    'roas': 0.0
                }
            
            platform_breakdown[platform]['impressions'] += analytics.total_impressions
            platform_breakdown[platform]['clicks'] += analytics.total_clicks
            platform_breakdown[platform]['conversions'] += analytics.total_conversions
            platform_breakdown[platform]['spend'] += analytics.total_spend
            platform_breakdown[platform]['revenue'] += analytics.total_revenue
        
        # Calculate derived metrics for each platform
        for platform, data in platform_breakdown.items():
            impressions = data['impressions']
            clicks = data['clicks']
            conversions = data['conversions']
            spend = data['spend']
            revenue = data['revenue']
            
            # Calculate CTR
            if impressions > 0:
                data['ctr'] = (clicks / impressions) * 100
            
            # Calculate CPC
            if clicks > 0:
                data['cpc'] = spend / clicks
            
            # Calculate CPM
            if impressions > 0:
                data['cpm'] = (spend / impressions) * 1000
            
            # Calculate conversion rate
            if clicks > 0:
                data['conversion_rate'] = (conversions / clicks) * 100
            
            # Calculate cost per conversion
            if conversions > 0:
                data['cost_per_conversion'] = spend / conversions
            
            # Calculate ROAS
            if spend > 0:
                data['roas'] = revenue / spend
        
        return platform_breakdown
    
    def _get_campaign_breakdown(self, analytics_list: List[CampaignAnalytics]) -> Dict:
        """
        Get campaign breakdown from analytics list
        
        Args:
            analytics_list (List[CampaignAnalytics]): Analytics list
            
        Returns:
            Dict: Campaign breakdown
        """
        campaign_breakdown = {}
        
        for analytics in analytics_list:
            campaign_id = str(analytics.campaign.id)
            campaign_name = analytics.campaign.name
            
            if campaign_id not in campaign_breakdown:
                campaign_breakdown[campaign_id] = {
                    'campaign_id': campaign_id,
                    'campaign_name': campaign_name,
                    'impressions': 0,
                    'clicks': 0,
                    'conversions': 0,
                    'spend': 0.0,
                    'revenue': 0.0,
                    'ctr': 0.0,
                    'cpc': 0.0,
                    'cpm': 0.0,
                    'conversion_rate': 0.0,
                    'cost_per_conversion': 0.0,
                    'roas': 0.0
                }
            
            campaign_breakdown[campaign_id]['impressions'] += analytics.total_impressions
            campaign_breakdown[campaign_id]['clicks'] += analytics.total_clicks
            campaign_breakdown[campaign_id]['conversions'] += analytics.total_conversions
            campaign_breakdown[campaign_id]['spend'] += analytics.total_spend
            campaign_breakdown[campaign_id]['revenue'] += analytics.total_revenue
        
        # Calculate derived metrics for each campaign
        for campaign_id, data in campaign_breakdown.items():
            impressions = data['impressions']
            clicks = data['clicks']
            conversions = data['conversions']
            spend = data['spend']
            revenue = data['revenue']
            
            # Calculate CTR
            if impressions > 0:
                data['ctr'] = (clicks / impressions) * 100
            
            # Calculate CPC
            if clicks > 0:
                data['cpc'] = spend / clicks
            
            # Calculate CPM
            if impressions > 0:
                data['cpm'] = (spend / impressions) * 1000
            
            # Calculate conversion rate
            if clicks > 0:
                data['conversion_rate'] = (conversions / clicks) * 100
            
            # Calculate cost per conversion
            if conversions > 0:
                data['cost_per_conversion'] = spend / conversions
            
            # Calculate ROAS
            if spend > 0:
                data['roas'] = revenue / spend
        
        return list(campaign_breakdown.values())
    
    def _get_recommendations(self, analytics_list: List[CampaignAnalytics]) -> List[Dict]:
        """
        Get recommendations from analytics list
        
        Args:
            analytics_list (List[CampaignAnalytics]): Analytics list
            
        Returns:
            List[Dict]: Recommendations
        """
        recommendations = []
        
        for analytics in analytics_list:
            recommendations.extend(analytics.get_recommendations())
        
        return recommendations
    
    def _create_campaign_analytics(self, user: User, campaign: Campaign, platform: str, 
                                  start_date: datetime, end_date: datetime, data: Dict) -> CampaignAnalytics:
        """
        Create campaign analytics object
        
        Args:
            user (User): User
            campaign (Campaign): Campaign
            platform (str): Platform
            start_date (datetime): Start date
            end_date (datetime): End date
            data (Dict): Analytics data
            
        Returns:
            CampaignAnalytics: Campaign analytics
        """
        # Create analytics object
        analytics = CampaignAnalytics(
            user=user,
            campaign=campaign,
            platform=platform,
            start_date=start_date,
            end_date=end_date,
            total_impressions=data.get('total_impressions', 0),
            total_clicks=data.get('total_clicks', 0),
            total_conversions=data.get('total_conversions', 0),
            total_spend=data.get('total_spend', 0.0),
            total_revenue=data.get('total_revenue', 0.0),
            average_ctr=data.get('average_ctr', 0.0),
            average_cpc=data.get('average_cpc', 0.0),
            average_cpm=data.get('average_cpm', 0.0),
            average_conversion_rate=data.get('average_conversion_rate', 0.0),
            average_cost_per_conversion=data.get('average_cost_per_conversion', 0.0),
            roas=data.get('roas', 0.0),
            last_updated=datetime.utcnow()
        )
        
        # Add daily metrics
        for daily_data in data.get('daily_metrics', []):
            daily_metric = DailyMetric(
                date=datetime.fromisoformat(daily_data['date']),
                impressions=daily_data.get('impressions', 0),
                clicks=daily_data.get('clicks', 0),
                conversions=daily_data.get('conversions', 0),
                spend=daily_data.get('spend', 0.0),
                ctr=daily_data.get('ctr', 0.0),
                cpc=daily_data.get('cpc', 0.0),
                cpm=daily_data.get('cpm', 0.0),
                conversion_rate=daily_data.get('conversion_rate', 0.0),
                cost_per_conversion=daily_data.get('cost_per_conversion', 0.0),
                roas=daily_data.get('roas', 0.0),
                engagement=daily_data.get('engagement', 0),
                reach=daily_data.get('reach', 0),
                frequency=daily_data.get('frequency', 0.0),
                video_views=daily_data.get('video_views', 0),
                video_view_rate=daily_data.get('video_view_rate', 0.0),
                add_to_cart=daily_data.get('add_to_cart', 0),
                purchases=daily_data.get('purchases', 0),
                revenue=daily_data.get('revenue', 0.0)
            )
            analytics.daily_metrics.append(daily_metric)
        
        # Add audience insights
        if 'audience_insights' in data:
            audience_data = data['audience_insights']
            
            audience_insights = AudienceInsight(
                age_gender=audience_data.get('age_gender', {}),
                locations=audience_data.get('locations', {}),
                interests=audience_data.get('interests', {}),
                behaviors=audience_data.get('behaviors', {}),
                devices=audience_data.get('devices', {}),
                platforms=audience_data.get('platforms', {}),
                placements=audience_data.get('placements', {}),
                time_of_day=audience_data.get('time_of_day', {}),
                day_of_week=audience_data.get('day_of_week', {})
            )
            analytics.audience_insights = audience_insights
        
        # Add creative performance
        for creative_data in data.get('creative_performance', []):
            creative_performance = CreativePerformance(
                creative_id=creative_data['creative_id'],
                impressions=creative_data.get('impressions', 0),
                clicks=creative_data.get('clicks', 0),
                conversions=creative_data.get('conversions', 0),
                spend=creative_data.get('spend', 0.0),
                ctr=creative_data.get('ctr', 0.0),
                cpc=creative_data.get('cpc', 0.0),
                cpm=creative_data.get('cpm', 0.0),
                conversion_rate=creative_data.get('conversion_rate', 0.0),
                cost_per_conversion=creative_data.get('cost_per_conversion', 0.0),
                engagement_rate=creative_data.get('engagement_rate', 0.0),
                video_view_rate=creative_data.get('video_view_rate', 0.0)
            )
            analytics.creative_performance.append(creative_performance)
        
        # Add recommendations
        for recommendation_data in data.get('recommendations', []):
            recommendation = Recommendation(
                id=recommendation_data.get('id', str(uuid.uuid4())),
                type=recommendation_data['type'],
                priority=recommendation_data.get('priority', 'medium'),
                description=recommendation_data['description'],
                expected_impact=recommendation_data.get('expected_impact', ''),
                status=recommendation_data.get('status', 'pending'),
                created_at=datetime.utcnow()
            )
            analytics.recommendations.append(recommendation)
        
        # Save analytics
        analytics.save()
        
        return analytics
    
    def _get_platform_connector(self, platform: str):
        """
        Get platform connector
        
        Args:
            platform (str): Platform name
            
        Returns:
            Object: Platform connector
        """
        if platform == 'facebook':
            return self.facebook_connector
        elif platform == 'instagram':
            return self.instagram_connector
        elif platform == 'tiktok':
            return self.tiktok_connector
        elif platform == 'shopee':
            return self.shopee_connector
        
        return None
