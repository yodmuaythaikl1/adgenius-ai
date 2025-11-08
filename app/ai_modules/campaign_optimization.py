"""
AdGenius AI Backend - Campaign Optimization AI Module
"""
import os
import json
import logging
import time
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    
try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

from app.utils.helpers import generate_id
from app.platform_connectors.facebook_connector import FacebookConnector
from app.platform_connectors.instagram_connector import InstagramConnector
from app.platform_connectors.tiktok_connector import TikTokConnector
from app.platform_connectors.shopee_connector import ShopeeConnector

logger = logging.getLogger(__name__)

class CampaignOptimizationAI:
    """Campaign Optimization AI Module"""
    
    def __init__(self):
        """Initialize Campaign Optimization AI"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.facebook_connector = FacebookConnector()
        self.instagram_connector = InstagramConnector()
        self.tiktok_connector = TikTokConnector()
        self.shopee_connector = ShopeeConnector()
        
        # Initialize OpenAI client
        openai.api_key = self.openai_api_key
    
    def analyze_campaign_performance(self, platform: str, campaign_id: str, access_token: str, account_id: str = None, start_date: datetime = None, end_date: datetime = None) -> Dict:
        """
        Analyze campaign performance
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            start_date (datetime, optional): Start date
            end_date (datetime, optional): End date
            
        Returns:
            Dict: Campaign performance analysis
        """
        try:
            # Set default dates if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            
            if not end_date:
                end_date = datetime.now()
            
            # Get platform-specific performance
            if platform == 'facebook':
                self.facebook_connector.initialize(access_token)
                return self._analyze_facebook_campaign(campaign_id, start_date, end_date)
            elif platform == 'instagram':
                self.instagram_connector.initialize(access_token)
                return self._analyze_instagram_campaign(campaign_id, start_date, end_date)
            elif platform == 'tiktok':
                self.tiktok_connector.initialize(access_token)
                return self._analyze_tiktok_campaign(account_id, campaign_id, start_date, end_date)
            elif platform == 'shopee':
                self.shopee_connector.initialize(access_token, account_id)
                return self._analyze_shopee_campaign(start_date, end_date)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error analyzing campaign performance: {str(e)}")
            return {'error': f"Error analyzing campaign performance: {str(e)}"}
    
    def optimize_campaign_budget(self, platform: str, campaign_id: str, access_token: str, account_id: str = None, total_budget: float = None) -> Dict:
        """
        Optimize campaign budget allocation
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized budget allocation
        """
        try:
            # Get campaign performance
            performance = self.analyze_campaign_performance(
                platform=platform,
                campaign_id=campaign_id,
                access_token=access_token,
                account_id=account_id
            )
            
            if 'error' in performance:
                return performance
            
            # Optimize budget based on platform
            if platform == 'facebook':
                return self._optimize_facebook_budget(performance, total_budget)
            elif platform == 'instagram':
                return self._optimize_instagram_budget(performance, total_budget)
            elif platform == 'tiktok':
                return self._optimize_tiktok_budget(performance, total_budget)
            elif platform == 'shopee':
                return self._optimize_shopee_budget(performance, total_budget)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error optimizing campaign budget: {str(e)}")
            return {'error': f"Error optimizing campaign budget: {str(e)}"}
    
    def optimize_campaign_schedule(self, platform: str, campaign_id: str, access_token: str, account_id: str = None) -> Dict:
        """
        Optimize campaign schedule
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            
        Returns:
            Dict: Optimized campaign schedule
        """
        try:
            # Get campaign performance
            performance = self.analyze_campaign_performance(
                platform=platform,
                campaign_id=campaign_id,
                access_token=access_token,
                account_id=account_id
            )
            
            if 'error' in performance:
                return performance
            
            # Optimize schedule based on platform
            if platform == 'facebook':
                return self._optimize_facebook_schedule(performance)
            elif platform == 'instagram':
                return self._optimize_instagram_schedule(performance)
            elif platform == 'tiktok':
                return self._optimize_tiktok_schedule(performance)
            elif platform == 'shopee':
                return self._optimize_shopee_schedule(performance)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error optimizing campaign schedule: {str(e)}")
            return {'error': f"Error optimizing campaign schedule: {str(e)}"}
    
    def optimize_campaign_bidding(self, platform: str, campaign_id: str, access_token: str, account_id: str = None) -> Dict:
        """
        Optimize campaign bidding strategy
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            
        Returns:
            Dict: Optimized bidding strategy
        """
        try:
            # Get campaign performance
            performance = self.analyze_campaign_performance(
                platform=platform,
                campaign_id=campaign_id,
                access_token=access_token,
                account_id=account_id
            )
            
            if 'error' in performance:
                return performance
            
            # Optimize bidding based on platform
            if platform == 'facebook':
                return self._optimize_facebook_bidding(performance)
            elif platform == 'instagram':
                return self._optimize_instagram_bidding(performance)
            elif platform == 'tiktok':
                return self._optimize_tiktok_bidding(performance)
            elif platform == 'shopee':
                return self._optimize_shopee_bidding(performance)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error optimizing campaign bidding: {str(e)}")
            return {'error': f"Error optimizing campaign bidding: {str(e)}"}
    
    def generate_campaign_recommendations(self, platform: str, campaign_id: str, access_token: str, account_id: str = None) -> Dict:
        """
        Generate campaign recommendations
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            
        Returns:
            Dict: Campaign recommendations
        """
        try:
            # Get campaign performance
            performance = self.analyze_campaign_performance(
                platform=platform,
                campaign_id=campaign_id,
                access_token=access_token,
                account_id=account_id
            )
            
            if 'error' in performance:
                return performance
            
            # Generate recommendations based on platform
            if platform == 'facebook':
                return self._generate_facebook_recommendations(performance)
            elif platform == 'instagram':
                return self._generate_instagram_recommendations(performance)
            elif platform == 'tiktok':
                return self._generate_tiktok_recommendations(performance)
            elif platform == 'shopee':
                return self._generate_shopee_recommendations(performance)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error generating campaign recommendations: {str(e)}")
            return {'error': f"Error generating campaign recommendations: {str(e)}"}
    
    def optimize_cross_platform_budget(self, platforms: List[str], campaign_ids: List[str], access_tokens: List[str], account_ids: List[str] = None, total_budget: float = None) -> Dict:
        """
        Optimize budget allocation across multiple platforms
        
        Args:
            platforms (List[str]): Platforms
            campaign_ids (List[str]): Campaign IDs
            access_tokens (List[str]): Access tokens
            account_ids (List[str], optional): Account IDs
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized cross-platform budget allocation
        """
        try:
            # Validate input
            if len(platforms) != len(campaign_ids) or len(platforms) != len(access_tokens):
                return {'error': 'Platforms, campaign IDs, and access tokens must have the same length'}
            
            if account_ids and len(platforms) != len(account_ids):
                return {'error': 'Platforms and account IDs must have the same length'}
            
            # Set default account IDs if not provided
            if not account_ids:
                account_ids = [None] * len(platforms)
            
            # Get performance for each platform
            performances = []
            
            for i, platform in enumerate(platforms):
                performance = self.analyze_campaign_performance(
                    platform=platform,
                    campaign_id=campaign_ids[i],
                    access_token=access_tokens[i],
                    account_id=account_ids[i]
                )
                
                if 'error' in performance:
                    return performance
                
                performances.append({
                    'platform': platform,
                    'campaign_id': campaign_ids[i],
                    'performance': performance
                })
            
            # Calculate performance metrics for each platform
            platform_metrics = []
            
            for item in performances:
                platform = item['platform']
                performance = item['performance']
                
                # Extract key metrics
                if platform in ['facebook', 'instagram', 'tiktok']:
                    impressions = performance.get('total_impressions', 0)
                    clicks = performance.get('total_clicks', 0)
                    conversions = performance.get('total_conversions', 0)
                    spend = performance.get('total_spend', 0)
                    
                    # Calculate derived metrics
                    ctr = (clicks / impressions * 100) if impressions > 0 else 0
                    cvr = (conversions / clicks * 100) if clicks > 0 else 0
                    cpc = spend / clicks if clicks > 0 else 0
                    cpa = spend / conversions if conversions > 0 else 0
                    roas = performance.get('total_revenue', 0) / spend if spend > 0 else 0
                elif platform == 'shopee':
                    impressions = performance.get('performance_metrics', {}).get('total_views', 0)
                    conversions = performance.get('performance_metrics', {}).get('total_orders', 0)
                    spend = 0  # Shopee doesn't have direct ad spend
                    
                    # Calculate derived metrics
                    cvr = (conversions / impressions * 100) if impressions > 0 else 0
                    ctr = cvr  # Use CVR as CTR for Shopee
                    cpc = 0
                    cpa = 0
                    roas = float('inf')  # No direct ad spend, so ROAS is infinite
                
                platform_metrics.append({
                    'platform': platform,
                    'campaign_id': item['campaign_id'],
                    'impressions': impressions,
                    'clicks': clicks if platform != 'shopee' else 0,
                    'conversions': conversions,
                    'spend': spend,
                    'ctr': ctr,
                    'cvr': cvr,
                    'cpc': cpc,
                    'cpa': cpa,
                    'roas': roas
                })
            
            # Calculate optimal budget allocation
            return self._optimize_cross_platform_budget(platform_metrics, total_budget)
        except Exception as e:
            logger.error(f"Error optimizing cross-platform budget: {str(e)}")
            return {'error': f"Error optimizing cross-platform budget: {str(e)}"}
    
    def generate_cross_platform_insights(self, platforms: List[str], campaign_ids: List[str], access_tokens: List[str], account_ids: List[str] = None) -> Dict:
        """
        Generate insights across multiple platforms
        
        Args:
            platforms (List[str]): Platforms
            campaign_ids (List[str]): Campaign IDs
            access_tokens (List[str]): Access tokens
            account_ids (List[str], optional): Account IDs
            
        Returns:
            Dict: Cross-platform insights
        """
        try:
            # Validate input
            if len(platforms) != len(campaign_ids) or len(platforms) != len(access_tokens):
                return {'error': 'Platforms, campaign IDs, and access tokens must have the same length'}
            
            if account_ids and len(platforms) != len(account_ids):
                return {'error': 'Platforms and account IDs must have the same length'}
            
            # Set default account IDs if not provided
            if not account_ids:
                account_ids = [None] * len(platforms)
            
            # Get performance for each platform
            performances = []
            
            for i, platform in enumerate(platforms):
                performance = self.analyze_campaign_performance(
                    platform=platform,
                    campaign_id=campaign_ids[i],
                    access_token=access_tokens[i],
                    account_id=account_ids[i]
                )
                
                if 'error' in performance:
                    return performance
                
                performances.append({
                    'platform': platform,
                    'campaign_id': campaign_ids[i],
                    'performance': performance
                })
            
            # Generate cross-platform insights
            return self._generate_cross_platform_insights(performances)
        except Exception as e:
            logger.error(f"Error generating cross-platform insights: {str(e)}")
            return {'error': f"Error generating cross-platform insights: {str(e)}"}
    
    def _analyze_facebook_campaign(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Facebook campaign
        
        Args:
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analysis
        """
        # Get campaign analytics
        analytics = self.facebook_connector.get_campaign_analytics(campaign_id, start_date, end_date)
        
        if 'error' in analytics:
            return analytics
        
        # Extract key metrics
        total_impressions = analytics.get('total_impressions', 0)
        total_clicks = analytics.get('total_clicks', 0)
        total_conversions = analytics.get('total_conversions', 0)
        total_spend = analytics.get('total_spend', 0)
        total_revenue = analytics.get('total_revenue', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        roas = total_revenue / total_spend if total_spend > 0 else 0
        
        # Extract daily metrics
        daily_metrics = analytics.get('daily_metrics', {})
        
        # Extract ad set metrics
        ad_set_metrics = analytics.get('ad_set_metrics', {})
        
        # Extract ad metrics
        ad_metrics = analytics.get('ad_metrics', {})
        
        # Extract audience insights
        audience_insights = analytics.get('audience_insights', {})
        
        return {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_spend': total_spend,
            'total_revenue': total_revenue,
            'ctr': ctr,
            'cvr': cvr,
            'cpc': cpc,
            'cpa': cpa,
            'roas': roas,
            'daily_metrics': daily_metrics,
            'ad_set_metrics': ad_set_metrics,
            'ad_metrics': ad_metrics,
            'audience_insights': audience_insights
        }
    
    def _analyze_instagram_campaign(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Instagram campaign
        
        Args:
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analysis
        """
        # Instagram uses Facebook's analytics
        return self._analyze_facebook_campaign(campaign_id, start_date, end_date)
    
    def _analyze_tiktok_campaign(self, advertiser_id: str, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze TikTok campaign
        
        Args:
            advertiser_id (str): Advertiser ID
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analysis
        """
        # Get campaign analytics
        analytics = self.tiktok_connector.get_campaign_analytics(advertiser_id, campaign_id, start_date, end_date)
        
        if 'error' in analytics:
            return analytics
        
        # Extract key metrics
        total_impressions = analytics.get('total_impressions', 0)
        total_clicks = analytics.get('total_clicks', 0)
        total_conversions = analytics.get('total_conversions', 0)
        total_spend = analytics.get('total_spend', 0)
        total_revenue = analytics.get('total_revenue', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        roas = total_revenue / total_spend if total_spend > 0 else 0
        
        # Extract daily metrics
        daily_metrics = analytics.get('daily_metrics', {})
        
        # Extract ad group metrics
        ad_group_metrics = analytics.get('ad_group_metrics', {})
        
        # Extract ad metrics
        ad_metrics = analytics.get('ad_metrics', {})
        
        # Extract audience insights
        audience_insights = analytics.get('audience_insights', {})
        
        # Extract video metrics
        video_metrics = analytics.get('video_metrics', {})
        
        return {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_spend': total_spend,
            'total_revenue': total_revenue,
            'ctr': ctr,
            'cvr': cvr,
            'cpc': cpc,
            'cpa': cpa,
            'roas': roas,
            'daily_metrics': daily_metrics,
            'ad_group_metrics': ad_group_metrics,
            'ad_metrics': ad_metrics,
            'audience_insights': audience_insights,
            'video_metrics': video_metrics
        }
    
    def _analyze_shopee_campaign(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Shopee campaign
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analysis
        """
        # Get shop performance
        performance = self.shopee_connector.get_shop_performance(start_date, end_date)
        
        if 'error' in performance:
            return performance
        
        return performance
    
    def _optimize_facebook_budget(self, performance: Dict, total_budget: float = None) -> Dict:
        """
        Optimize Facebook budget allocation
        
        Args:
            performance (Dict): Performance data
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized budget allocation
        """
        # Extract ad set metrics
        ad_set_metrics = performance.get('ad_set_metrics', {})
        
        if not ad_set_metrics:
            return {'error': 'No ad set metrics available'}
        
        # Calculate performance metrics for each ad set
        ad_set_performance = []
        
        for ad_set_id, metrics in ad_set_metrics.items():
            impressions = metrics.get('impressions', 0)
            clicks = metrics.get('clicks', 0)
            conversions = metrics.get('conversions', 0)
            spend = metrics.get('spend', 0)
            revenue = metrics.get('revenue', 0)
            
            # Calculate derived metrics
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cvr = (conversions / clicks * 100) if clicks > 0 else 0
            cpc = spend / clicks if clicks > 0 else 0
            cpa = spend / conversions if conversions > 0 else 0
            roas = revenue / spend if spend > 0 else 0
            
            ad_set_performance.append({
                'ad_set_id': ad_set_id,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend,
                'revenue': revenue,
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            })
        
        # Sort ad sets by ROAS
        ad_set_performance.sort(key=lambda x: x['roas'], reverse=True)
        
        # Calculate total spend
        total_spend = performance.get('total_spend', 0)
        
        # Set default total budget if not provided
        if not total_budget:
            total_budget = total_spend
        
        # Calculate budget allocation
        budget_allocation = []
        
        # Allocate budget based on ROAS
        total_roas = sum(ad_set['roas'] for ad_set in ad_set_performance)
        
        for ad_set in ad_set_performance:
            if total_roas > 0:
                allocation_percentage = ad_set['roas'] / total_roas
            else:
                allocation_percentage = 1 / len(ad_set_performance)
            
            allocated_budget = total_budget * allocation_percentage
            
            budget_allocation.append({
                'ad_set_id': ad_set['ad_set_id'],
                'current_spend': ad_set['spend'],
                'allocated_budget': allocated_budget,
                'allocation_percentage': allocation_percentage * 100,
                'roas': ad_set['roas'],
                'cpa': ad_set['cpa']
            })
        
        return {
            'total_budget': total_budget,
            'budget_allocation': budget_allocation
        }
    
    def _optimize_instagram_budget(self, performance: Dict, total_budget: float = None) -> Dict:
        """
        Optimize Instagram budget allocation
        
        Args:
            performance (Dict): Performance data
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized budget allocation
        """
        # Instagram uses Facebook's budget optimization
        return self._optimize_facebook_budget(performance, total_budget)
    
    def _optimize_tiktok_budget(self, performance: Dict, total_budget: float = None) -> Dict:
        """
        Optimize TikTok budget allocation
        
        Args:
            performance (Dict): Performance data
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized budget allocation
        """
        # Extract ad group metrics
        ad_group_metrics = performance.get('ad_group_metrics', {})
        
        if not ad_group_metrics:
            return {'error': 'No ad group metrics available'}
        
        # Calculate performance metrics for each ad group
        ad_group_performance = []
        
        for ad_group_id, metrics in ad_group_metrics.items():
            impressions = metrics.get('impressions', 0)
            clicks = metrics.get('clicks', 0)
            conversions = metrics.get('conversions', 0)
            spend = metrics.get('spend', 0)
            revenue = metrics.get('revenue', 0)
            
            # Calculate derived metrics
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cvr = (conversions / clicks * 100) if clicks > 0 else 0
            cpc = spend / clicks if clicks > 0 else 0
            cpa = spend / conversions if conversions > 0 else 0
            roas = revenue / spend if spend > 0 else 0
            
            ad_group_performance.append({
                'ad_group_id': ad_group_id,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend,
                'revenue': revenue,
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            })
        
        # Sort ad groups by ROAS
        ad_group_performance.sort(key=lambda x: x['roas'], reverse=True)
        
        # Calculate total spend
        total_spend = performance.get('total_spend', 0)
        
        # Set default total budget if not provided
        if not total_budget:
            total_budget = total_spend
        
        # Calculate budget allocation
        budget_allocation = []
        
        # Allocate budget based on ROAS
        total_roas = sum(ad_group['roas'] for ad_group in ad_group_performance)
        
        for ad_group in ad_group_performance:
            if total_roas > 0:
                allocation_percentage = ad_group['roas'] / total_roas
            else:
                allocation_percentage = 1 / len(ad_group_performance)
            
            allocated_budget = total_budget * allocation_percentage
            
            budget_allocation.append({
                'ad_group_id': ad_group['ad_group_id'],
                'current_spend': ad_group['spend'],
                'allocated_budget': allocated_budget,
                'allocation_percentage': allocation_percentage * 100,
                'roas': ad_group['roas'],
                'cpa': ad_group['cpa']
            })
        
        return {
            'total_budget': total_budget,
            'budget_allocation': budget_allocation
        }
    
    def _optimize_shopee_budget(self, performance: Dict, total_budget: float = None) -> Dict:
        """
        Optimize Shopee budget allocation
        
        Args:
            performance (Dict): Performance data
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized budget allocation
        """
        # Shopee doesn't have traditional ad budget allocation
        # Instead, we'll recommend product promotion budget
        
        # Set default total budget if not provided
        if not total_budget:
            total_budget = 100  # Default budget
        
        # Calculate budget allocation
        budget_allocation = []
        
        # Allocate budget based on product performance
        product_performance = performance.get('product_performance', [])
        
        if not product_performance:
            return {'error': 'No product performance data available'}
        
        # Sort products by conversion rate
        product_performance.sort(key=lambda x: x.get('conversion_rate', 0), reverse=True)
        
        # Calculate total conversion rate
        total_conversion_rate = sum(product.get('conversion_rate', 0) for product in product_performance)
        
        for product in product_performance:
            if total_conversion_rate > 0:
                allocation_percentage = product.get('conversion_rate', 0) / total_conversion_rate
            else:
                allocation_percentage = 1 / len(product_performance)
            
            allocated_budget = total_budget * allocation_percentage
            
            budget_allocation.append({
                'product_id': product.get('product_id'),
                'product_name': product.get('product_name'),
                'allocated_budget': allocated_budget,
                'allocation_percentage': allocation_percentage * 100,
                'conversion_rate': product.get('conversion_rate', 0),
                'recommended_promotion_type': 'daily_discover' if allocation_percentage > 0.2 else 'flash_sale'
            })
        
        return {
            'total_budget': total_budget,
            'budget_allocation': budget_allocation
        }
    
    def _optimize_facebook_schedule(self, performance: Dict) -> Dict:
        """
        Optimize Facebook campaign schedule
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized campaign schedule
        """
        # Extract daily metrics
        daily_metrics = performance.get('daily_metrics', {})
        
        if not daily_metrics:
            return {'error': 'No daily metrics available'}
        
        # Calculate performance metrics for each day of the week
        day_of_week_performance = {
            'Monday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Tuesday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Wednesday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Thursday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Friday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Saturday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Sunday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0}
        }
        
        # Calculate performance metrics for each hour of the day
        hour_of_day_performance = {str(hour): {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0} for hour in range(24)}
        
        # Process daily metrics
        for date_str, metrics in daily_metrics.items():
            # Parse date
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Get day of week
            day_of_week = date.strftime('%A')
            
            # Update day of week metrics
            day_of_week_performance[day_of_week]['impressions'] += metrics.get('impressions', 0)
            day_of_week_performance[day_of_week]['clicks'] += metrics.get('clicks', 0)
            day_of_week_performance[day_of_week]['conversions'] += metrics.get('conversions', 0)
            day_of_week_performance[day_of_week]['spend'] += metrics.get('spend', 0)
            day_of_week_performance[day_of_week]['count'] += 1
            
            # Process hourly metrics
            hourly_metrics = metrics.get('hourly_metrics', {})
            
            for hour, hour_metrics in hourly_metrics.items():
                hour_of_day_performance[hour]['impressions'] += hour_metrics.get('impressions', 0)
                hour_of_day_performance[hour]['clicks'] += hour_metrics.get('clicks', 0)
                hour_of_day_performance[hour]['conversions'] += hour_metrics.get('conversions', 0)
                hour_of_day_performance[hour]['spend'] += hour_metrics.get('spend', 0)
                hour_of_day_performance[hour]['count'] += 1
        
        # Calculate average metrics for each day of the week
        for day, metrics in day_of_week_performance.items():
            if metrics['count'] > 0:
                metrics['avg_impressions'] = metrics['impressions'] / metrics['count']
                metrics['avg_clicks'] = metrics['clicks'] / metrics['count']
                metrics['avg_conversions'] = metrics['conversions'] / metrics['count']
                metrics['avg_spend'] = metrics['spend'] / metrics['count']
                metrics['avg_ctr'] = (metrics['avg_clicks'] / metrics['avg_impressions'] * 100) if metrics['avg_impressions'] > 0 else 0
                metrics['avg_cvr'] = (metrics['avg_conversions'] / metrics['avg_clicks'] * 100) if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpc'] = metrics['avg_spend'] / metrics['avg_clicks'] if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpa'] = metrics['avg_spend'] / metrics['avg_conversions'] if metrics['avg_conversions'] > 0 else 0
        
        # Calculate average metrics for each hour of the day
        for hour, metrics in hour_of_day_performance.items():
            if metrics['count'] > 0:
                metrics['avg_impressions'] = metrics['impressions'] / metrics['count']
                metrics['avg_clicks'] = metrics['clicks'] / metrics['count']
                metrics['avg_conversions'] = metrics['conversions'] / metrics['count']
                metrics['avg_spend'] = metrics['spend'] / metrics['count']
                metrics['avg_ctr'] = (metrics['avg_clicks'] / metrics['avg_impressions'] * 100) if metrics['avg_impressions'] > 0 else 0
                metrics['avg_cvr'] = (metrics['avg_conversions'] / metrics['avg_clicks'] * 100) if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpc'] = metrics['avg_spend'] / metrics['avg_clicks'] if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpa'] = metrics['avg_spend'] / metrics['avg_conversions'] if metrics['avg_conversions'] > 0 else 0
        
        # Sort days by average CVR
        sorted_days = sorted(day_of_week_performance.items(), key=lambda x: x[1].get('avg_cvr', 0), reverse=True)
        
        # Sort hours by average CVR
        sorted_hours = sorted(hour_of_day_performance.items(), key=lambda x: x[1].get('avg_cvr', 0), reverse=True)
        
        # Get top 3 days
        top_days = [day for day, _ in sorted_days[:3]]
        
        # Get top 6 hours
        top_hours = [int(hour) for hour, _ in sorted_hours[:6]]
        top_hours.sort()
        
        # Create schedule
        schedule = {
            'top_days': top_days,
            'top_hours': top_hours,
            'day_of_week_performance': {day: metrics for day, metrics in sorted_days},
            'hour_of_day_performance': {hour: metrics for hour, metrics in sorted_hours}
        }
        
        return schedule
    
    def _optimize_instagram_schedule(self, performance: Dict) -> Dict:
        """
        Optimize Instagram campaign schedule
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized campaign schedule
        """
        # Instagram uses Facebook's schedule optimization
        return self._optimize_facebook_schedule(performance)
    
    def _optimize_tiktok_schedule(self, performance: Dict) -> Dict:
        """
        Optimize TikTok campaign schedule
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized campaign schedule
        """
        # Extract daily metrics
        daily_metrics = performance.get('daily_metrics', {})
        
        if not daily_metrics:
            return {'error': 'No daily metrics available'}
        
        # Calculate performance metrics for each day of the week
        day_of_week_performance = {
            'Monday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Tuesday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Wednesday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Thursday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Friday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Saturday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0},
            'Sunday': {'impressions': 0, 'clicks': 0, 'conversions': 0, 'spend': 0, 'count': 0}
        }
        
        # Process daily metrics
        for date_str, metrics in daily_metrics.items():
            # Parse date
            date = datetime.strptime(date_str, '%Y-%m-%d')
            
            # Get day of week
            day_of_week = date.strftime('%A')
            
            # Update day of week metrics
            day_of_week_performance[day_of_week]['impressions'] += metrics.get('impressions', 0)
            day_of_week_performance[day_of_week]['clicks'] += metrics.get('clicks', 0)
            day_of_week_performance[day_of_week]['conversions'] += metrics.get('conversions', 0)
            day_of_week_performance[day_of_week]['spend'] += metrics.get('spend', 0)
            day_of_week_performance[day_of_week]['count'] += 1
        
        # Calculate average metrics for each day of the week
        for day, metrics in day_of_week_performance.items():
            if metrics['count'] > 0:
                metrics['avg_impressions'] = metrics['impressions'] / metrics['count']
                metrics['avg_clicks'] = metrics['clicks'] / metrics['count']
                metrics['avg_conversions'] = metrics['conversions'] / metrics['count']
                metrics['avg_spend'] = metrics['spend'] / metrics['count']
                metrics['avg_ctr'] = (metrics['avg_clicks'] / metrics['avg_impressions'] * 100) if metrics['avg_impressions'] > 0 else 0
                metrics['avg_cvr'] = (metrics['avg_conversions'] / metrics['avg_clicks'] * 100) if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpc'] = metrics['avg_spend'] / metrics['avg_clicks'] if metrics['avg_clicks'] > 0 else 0
                metrics['avg_cpa'] = metrics['avg_spend'] / metrics['avg_conversions'] if metrics['avg_conversions'] > 0 else 0
        
        # Sort days by average CVR
        sorted_days = sorted(day_of_week_performance.items(), key=lambda x: x[1].get('avg_cvr', 0), reverse=True)
        
        # Get top 3 days
        top_days = [day for day, _ in sorted_days[:3]]
        
        # TikTok-specific optimal hours (based on general TikTok usage patterns)
        top_hours = [9, 12, 15, 18, 21, 22]
        
        # Create schedule
        schedule = {
            'top_days': top_days,
            'top_hours': top_hours,
            'day_of_week_performance': {day: metrics for day, metrics in sorted_days}
        }
        
        return schedule
    
    def _optimize_shopee_schedule(self, performance: Dict) -> Dict:
        """
        Optimize Shopee campaign schedule
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized campaign schedule
        """
        # Shopee doesn't have traditional campaign scheduling
        # Instead, we'll recommend optimal times for promotions
        
        # Shopee-specific optimal days (based on general e-commerce patterns)
        top_days = ['Monday', 'Wednesday', 'Friday']
        
        # Shopee-specific optimal hours (based on general e-commerce patterns)
        top_hours = [9, 12, 15, 18, 21, 22]
        
        # Create schedule
        schedule = {
            'top_days': top_days,
            'top_hours': top_hours,
            'recommended_promotion_schedule': [
                {
                    'promotion_type': 'flash_sale',
                    'days': ['Monday', 'Friday'],
                    'hours': [12, 18, 21]
                },
                {
                    'promotion_type': 'daily_discover',
                    'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                    'hours': [9, 15, 21]
                }
            ]
        }
        
        return schedule
    
    def _optimize_facebook_bidding(self, performance: Dict) -> Dict:
        """
        Optimize Facebook bidding strategy
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized bidding strategy
        """
        # Extract key metrics
        total_impressions = performance.get('total_impressions', 0)
        total_clicks = performance.get('total_clicks', 0)
        total_conversions = performance.get('total_conversions', 0)
        total_spend = performance.get('total_spend', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        
        # Determine optimal bidding strategy
        if cvr > 2.0:
            # High conversion rate, focus on conversions
            bidding_strategy = 'LOWEST_COST_WITH_BID_CAP'
            bid_cap = cpa * 1.2  # Set bid cap 20% higher than current CPA
            optimization_goal = 'CONVERSIONS'
        elif ctr > 1.0:
            # Good click-through rate, focus on clicks
            bidding_strategy = 'LOWEST_COST_WITHOUT_CAP'
            bid_cap = None
            optimization_goal = 'LINK_CLICKS'
        else:
            # Low performance, focus on reach and impressions
            bidding_strategy = 'LOWEST_COST_WITHOUT_CAP'
            bid_cap = None
            optimization_goal = 'REACH'
        
        return {
            'bidding_strategy': bidding_strategy,
            'bid_cap': bid_cap,
            'optimization_goal': optimization_goal,
            'current_metrics': {
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa
            }
        }
    
    def _optimize_instagram_bidding(self, performance: Dict) -> Dict:
        """
        Optimize Instagram bidding strategy
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized bidding strategy
        """
        # Instagram uses Facebook's bidding optimization
        return self._optimize_facebook_bidding(performance)
    
    def _optimize_tiktok_bidding(self, performance: Dict) -> Dict:
        """
        Optimize TikTok bidding strategy
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized bidding strategy
        """
        # Extract key metrics
        total_impressions = performance.get('total_impressions', 0)
        total_clicks = performance.get('total_clicks', 0)
        total_conversions = performance.get('total_conversions', 0)
        total_spend = performance.get('total_spend', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        
        # Determine optimal bidding strategy
        if cvr > 2.0:
            # High conversion rate, focus on conversions
            bidding_strategy = 'BID_TYPE_CUSTOM'
            bid_value = cpa * 1.2  # Set bid 20% higher than current CPA
            optimization_goal = 'CONVERSION'
        elif ctr > 1.0:
            # Good click-through rate, focus on clicks
            bidding_strategy = 'BID_TYPE_NO_BID'
            bid_value = None
            optimization_goal = 'CLICK'
        else:
            # Low performance, focus on reach and impressions
            bidding_strategy = 'BID_TYPE_NO_BID'
            bid_value = None
            optimization_goal = 'REACH'
        
        return {
            'bidding_strategy': bidding_strategy,
            'bid_value': bid_value,
            'optimization_goal': optimization_goal,
            'current_metrics': {
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa
            }
        }
    
    def _optimize_shopee_bidding(self, performance: Dict) -> Dict:
        """
        Optimize Shopee bidding strategy
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized bidding strategy
        """
        # Shopee doesn't have traditional bidding
        # Instead, we'll recommend promotion strategies
        
        # Extract metrics
        total_views = performance.get('performance_metrics', {}).get('total_views', 0)
        total_orders = performance.get('performance_metrics', {}).get('total_orders', 0)
        
        # Calculate conversion rate
        conversion_rate = (total_orders / total_views * 100) if total_views > 0 else 0
        
        # Determine optimal promotion strategy
        if conversion_rate > 5.0:
            # High conversion rate, focus on visibility
            promotion_strategy = 'daily_discover'
            boost_frequency = 'daily'
            discount_percentage = 5
        elif conversion_rate > 2.0:
            # Moderate conversion rate, focus on conversions
            promotion_strategy = 'flash_sale'
            boost_frequency = 'twice_daily'
            discount_percentage = 10
        else:
            # Low conversion rate, focus on attracting customers
            promotion_strategy = 'flash_sale'
            boost_frequency = 'three_times_daily'
            discount_percentage = 15
        
        return {
            'promotion_strategy': promotion_strategy,
            'boost_frequency': boost_frequency,
            'discount_percentage': discount_percentage,
            'current_metrics': {
                'conversion_rate': conversion_rate
            }
        }
    
    def _generate_facebook_recommendations(self, performance: Dict) -> Dict:
        """
        Generate Facebook campaign recommendations
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Campaign recommendations
        """
        # Extract key metrics
        total_impressions = performance.get('total_impressions', 0)
        total_clicks = performance.get('total_clicks', 0)
        total_conversions = performance.get('total_conversions', 0)
        total_spend = performance.get('total_spend', 0)
        total_revenue = performance.get('total_revenue', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        roas = total_revenue / total_spend if total_spend > 0 else 0
        
        # Generate recommendations
        recommendations = []
        
        # CTR recommendations
        if ctr < 1.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'creative',
                'priority': 'high',
                'description': 'Your click-through rate (CTR) is below average. Consider testing new ad creatives with more compelling headlines and images.',
                'expected_impact': 'Increasing CTR can lead to more clicks and potentially more conversions.'
            })
        
        # CVR recommendations
        if cvr < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'landing_page',
                'priority': 'high',
                'description': 'Your conversion rate (CVR) is below average. Consider optimizing your landing page for better user experience and clearer call-to-action.',
                'expected_impact': 'Improving CVR can lead to more conversions without increasing ad spend.'
            })
        
        # Budget recommendations
        if roas < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'budget',
                'priority': 'medium',
                'description': 'Your return on ad spend (ROAS) is below target. Consider reallocating budget to better performing ad sets.',
                'expected_impact': 'Optimizing budget allocation can improve overall campaign ROAS.'
            })
        
        # Audience recommendations
        audience_insights = performance.get('audience_insights', {})
        
        if audience_insights:
            # Check if there are clear high-performing segments
            age_gender = audience_insights.get('age_gender', {})
            
            if age_gender:
                best_segment = max(age_gender.items(), key=lambda x: x[1].get('ctr', 0)) if age_gender else ('unknown', {})
                
                recommendations.append({
                    'id': generate_id(),
                    'type': 'audience',
                    'priority': 'medium',
                    'description': f"Your best performing audience segment is {best_segment[0]}. Consider creating a separate campaign targeting this segment specifically.",
                    'expected_impact': 'Focusing on high-performing segments can improve overall campaign performance.'
                })
        
        # Schedule recommendations
        daily_metrics = performance.get('daily_metrics', {})
        
        if daily_metrics:
            # Optimize schedule
            schedule = self._optimize_facebook_schedule(performance)
            
            recommendations.append({
                'id': generate_id(),
                'type': 'schedule',
                'priority': 'low',
                'description': f"Your ads perform best on {', '.join(schedule.get('top_days', []))} between {min(schedule.get('top_hours', []))}:00 and {max(schedule.get('top_hours', []))}:00. Consider adjusting your ad schedule to focus on these times.",
                'expected_impact': 'Scheduling ads during high-performing times can improve overall campaign efficiency.'
            })
        
        # Bidding recommendations
        bidding = self._optimize_facebook_bidding(performance)
        
        recommendations.append({
            'id': generate_id(),
            'type': 'bidding',
            'priority': 'medium',
            'description': f"Based on your campaign performance, we recommend using {bidding.get('bidding_strategy')} bidding strategy with {bidding.get('optimization_goal')} optimization goal.",
            'expected_impact': 'Optimizing bidding strategy can improve campaign efficiency and reduce costs.'
        })
        
        return {
            'recommendations': recommendations,
            'performance_summary': {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'conversions': total_conversions,
                'spend': total_spend,
                'revenue': total_revenue,
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            }
        }
    
    def _generate_instagram_recommendations(self, performance: Dict) -> Dict:
        """
        Generate Instagram campaign recommendations
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Campaign recommendations
        """
        # Get Facebook recommendations
        facebook_recommendations = self._generate_facebook_recommendations(performance)
        
        # Add Instagram-specific recommendations
        recommendations = facebook_recommendations.get('recommendations', [])
        
        # Add hashtag recommendation
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'medium',
            'description': 'Consider using popular and relevant hashtags in your Instagram ads to increase visibility.',
            'expected_impact': 'Using effective hashtags can extend the reach of your ads beyond your target audience.'
        })
        
        # Add visual content recommendation
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'high',
            'description': 'Instagram is a visual platform. Ensure your ads have high-quality, eye-catching images or videos that stand out in users\' feeds.',
            'expected_impact': 'Visually appealing content can significantly improve engagement and click-through rates on Instagram.'
        })
        
        # Add story ads recommendation
        recommendations.append({
            'id': generate_id(),
            'type': 'placement',
            'priority': 'medium',
            'description': 'Consider using Instagram Stories ads in addition to feed ads. Stories have high visibility and engagement rates.',
            'expected_impact': 'Adding Stories placement can reach users who may not engage with feed content.'
        })
        
        # Update recommendations
        facebook_recommendations['recommendations'] = recommendations
        
        return facebook_recommendations
    
    def _generate_tiktok_recommendations(self, performance: Dict) -> Dict:
        """
        Generate TikTok campaign recommendations
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Campaign recommendations
        """
        # Extract key metrics
        total_impressions = performance.get('total_impressions', 0)
        total_clicks = performance.get('total_clicks', 0)
        total_conversions = performance.get('total_conversions', 0)
        total_spend = performance.get('total_spend', 0)
        total_revenue = performance.get('total_revenue', 0)
        
        # Calculate derived metrics
        ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        cpc = total_spend / total_clicks if total_clicks > 0 else 0
        cpa = total_spend / total_conversions if total_conversions > 0 else 0
        roas = total_revenue / total_spend if total_spend > 0 else 0
        
        # Generate recommendations
        recommendations = []
        
        # Video metrics recommendations
        video_metrics = performance.get('video_metrics', {})
        
        if video_metrics:
            completion_rate = video_metrics.get('completion_rate', 0)
            
            if completion_rate < 50:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'creative',
                    'priority': 'high',
                    'description': 'Your video completion rate is below average. Consider creating shorter, more engaging videos that capture attention in the first 3 seconds.',
                    'expected_impact': 'Higher video completion rates can lead to better engagement and conversion rates.'
                })
        
        # CTR recommendations
        if ctr < 1.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'creative',
                'priority': 'high',
                'description': 'Your click-through rate (CTR) is below average. Consider using trending sounds, effects, or challenges in your TikTok ads to increase engagement.',
                'expected_impact': 'Using trending elements can significantly improve CTR on TikTok.'
            })
        
        # CVR recommendations
        if cvr < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'landing_page',
                'priority': 'high',
                'description': 'Your conversion rate (CVR) is below average. Ensure your landing page experience matches the style and tone of your TikTok ads for a seamless user journey.',
                'expected_impact': 'A consistent user experience can improve conversion rates.'
            })
        
        # Budget recommendations
        if roas < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'budget',
                'priority': 'medium',
                'description': 'Your return on ad spend (ROAS) is below target. Consider reallocating budget to better performing ad groups.',
                'expected_impact': 'Optimizing budget allocation can improve overall campaign ROAS.'
            })
        
        # TikTok-specific recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'medium',
            'description': 'TikTok users prefer authentic, native-looking content. Consider creating ads that look like organic TikTok content rather than traditional ads.',
            'expected_impact': 'Native-looking content typically performs better on TikTok.'
        })
        
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'medium',
            'description': 'Consider partnering with TikTok creators for Spark Ads, which allow you to boost organic content from creators.',
            'expected_impact': 'Spark Ads often have higher engagement rates than traditional ads.'
        })
        
        # Schedule recommendations
        schedule = self._optimize_tiktok_schedule(performance)
        
        recommendations.append({
            'id': generate_id(),
            'type': 'schedule',
            'priority': 'low',
            'description': f"Your ads perform best on {', '.join(schedule.get('top_days', []))} between {min(schedule.get('top_hours', []))}:00 and {max(schedule.get('top_hours', []))}:00. Consider adjusting your ad schedule to focus on these times.",
            'expected_impact': 'Scheduling ads during high-performing times can improve overall campaign efficiency.'
        })
        
        # Bidding recommendations
        bidding = self._optimize_tiktok_bidding(performance)
        
        recommendations.append({
            'id': generate_id(),
            'type': 'bidding',
            'priority': 'medium',
            'description': f"Based on your campaign performance, we recommend using {bidding.get('bidding_strategy')} bidding strategy with {bidding.get('optimization_goal')} optimization goal.",
            'expected_impact': 'Optimizing bidding strategy can improve campaign efficiency and reduce costs.'
        })
        
        return {
            'recommendations': recommendations,
            'performance_summary': {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'conversions': total_conversions,
                'spend': total_spend,
                'revenue': total_revenue,
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            }
        }
    
    def _generate_shopee_recommendations(self, performance: Dict) -> Dict:
        """
        Generate Shopee campaign recommendations
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Campaign recommendations
        """
        # Extract metrics
        total_views = performance.get('performance_metrics', {}).get('total_views', 0)
        total_orders = performance.get('performance_metrics', {}).get('total_orders', 0)
        total_revenue = performance.get('performance_metrics', {}).get('total_revenue', 0)
        conversion_rate = performance.get('performance_metrics', {}).get('conversion_rate', 0)
        
        # Generate recommendations
        recommendations = []
        
        # Conversion rate recommendations
        if conversion_rate < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'product_listing',
                'priority': 'high',
                'description': 'Your conversion rate is below average. Consider optimizing your product listings with better images, more detailed descriptions, and competitive pricing.',
                'expected_impact': 'Improved product listings can significantly increase conversion rates.'
            })
        
        # Product recommendations
        product_performance = performance.get('product_performance', [])
        
        if product_performance:
            # Find best and worst performing products
            best_product = max(product_performance, key=lambda x: x.get('conversion_rate', 0))
            worst_product = min(product_performance, key=lambda x: x.get('conversion_rate', 0))
            
            # If there's a significant difference
            if best_product.get('conversion_rate', 0) > worst_product.get('conversion_rate', 0) * 2:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'product_optimization',
                    'priority': 'medium',
                    'description': f"There's a significant performance gap between your products. Consider optimizing the listing for '{worst_product.get('product_name')}' based on what works for '{best_product.get('product_name')}'.",
                    'expected_impact': 'Improving low-performing products can increase overall shop performance.'
                })
        
        # Promotion recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'promotion',
            'priority': 'medium',
            'description': 'Participate in Shopee campaigns and promotions to increase visibility and sales.',
            'expected_impact': 'Shopee campaigns can drive significant traffic and sales.'
        })
        
        # Boost recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'visibility',
            'priority': 'medium',
            'description': 'Use Shopee Boost feature for your best-selling products to increase visibility.',
            'expected_impact': 'Boosted products appear higher in search results, driving more traffic and sales.'
        })
        
        # Schedule recommendations
        schedule = self._optimize_shopee_schedule(performance)
        
        for promotion in schedule.get('recommended_promotion_schedule', []):
            recommendations.append({
                'id': generate_id(),
                'type': 'schedule',
                'priority': 'low',
                'description': f"Schedule {promotion.get('promotion_type')} promotions on {', '.join(promotion.get('days', []))} at {', '.join([f'{hour}:00' for hour in promotion.get('hours', [])])}.",
                'expected_impact': 'Scheduling promotions during high-traffic times can improve visibility and sales.'
            })
        
        # Pricing recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'pricing',
            'priority': 'medium',
            'description': 'Consider offering bundle deals or volume discounts to increase average order value.',
            'expected_impact': 'Bundle deals can increase average order value and overall revenue.'
        })
        
        return {
            'recommendations': recommendations,
            'performance_summary': {
                'views': total_views,
                'orders': total_orders,
                'revenue': total_revenue,
                'conversion_rate': conversion_rate
            }
        }
    
    def _optimize_cross_platform_budget(self, platform_metrics: List[Dict], total_budget: float = None) -> Dict:
        """
        Optimize budget allocation across multiple platforms
        
        Args:
            platform_metrics (List[Dict]): Platform metrics
            total_budget (float, optional): Total budget
            
        Returns:
            Dict: Optimized cross-platform budget allocation
        """
        # Calculate total spend
        total_spend = sum(platform['spend'] for platform in platform_metrics)
        
        # Set default total budget if not provided
        if not total_budget:
            total_budget = total_spend
        
        # Calculate budget allocation
        budget_allocation = []
        
        # Calculate performance score for each platform
        for platform in platform_metrics:
            # Calculate performance score based on ROAS and CVR
            # Higher score means better performance
            roas_weight = 0.7
            cvr_weight = 0.3
            
            performance_score = (platform['roas'] * roas_weight) + (platform['cvr'] * cvr_weight)
            platform['performance_score'] = performance_score
        
        # Sort platforms by performance score
        platform_metrics.sort(key=lambda x: x['performance_score'], reverse=True)
        
        # Calculate total performance score
        total_performance_score = sum(platform['performance_score'] for platform in platform_metrics)
        
        # Allocate budget based on performance score
        for platform in platform_metrics:
            if total_performance_score > 0:
                allocation_percentage = platform['performance_score'] / total_performance_score
            else:
                allocation_percentage = 1 / len(platform_metrics)
            
            allocated_budget = total_budget * allocation_percentage
            
            budget_allocation.append({
                'platform': platform['platform'],
                'campaign_id': platform['campaign_id'],
                'current_spend': platform['spend'],
                'allocated_budget': allocated_budget,
                'allocation_percentage': allocation_percentage * 100,
                'performance_score': platform['performance_score'],
                'roas': platform['roas'],
                'cvr': platform['cvr']
            })
        
        return {
            'total_budget': total_budget,
            'budget_allocation': budget_allocation
        }
    
    def _generate_cross_platform_insights(self, performances: List[Dict]) -> Dict:
        """
        Generate insights across multiple platforms
        
        Args:
            performances (List[Dict]): Platform performances
            
        Returns:
            Dict: Cross-platform insights
        """
        # Extract platform metrics
        platform_metrics = []
        
        for item in performances:
            platform = item['platform']
            performance = item['performance']
            
            # Extract key metrics
            if platform in ['facebook', 'instagram', 'tiktok']:
                impressions = performance.get('total_impressions', 0)
                clicks = performance.get('total_clicks', 0)
                conversions = performance.get('total_conversions', 0)
                spend = performance.get('total_spend', 0)
                revenue = performance.get('total_revenue', 0)
                
                # Calculate derived metrics
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                cvr = (conversions / clicks * 100) if clicks > 0 else 0
                cpc = spend / clicks if clicks > 0 else 0
                cpa = spend / conversions if conversions > 0 else 0
                roas = revenue / spend if spend > 0 else 0
            elif platform == 'shopee':
                impressions = performance.get('performance_metrics', {}).get('total_views', 0)
                conversions = performance.get('performance_metrics', {}).get('total_orders', 0)
                revenue = performance.get('performance_metrics', {}).get('total_revenue', 0)
                spend = 0  # Shopee doesn't have direct ad spend
                clicks = 0
                
                # Calculate derived metrics
                cvr = (conversions / impressions * 100) if impressions > 0 else 0
                ctr = 0
                cpc = 0
                cpa = 0
                roas = float('inf')  # No direct ad spend, so ROAS is infinite
            
            platform_metrics.append({
                'platform': platform,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'spend': spend,
                'revenue': revenue,
                'ctr': ctr,
                'cvr': cvr,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            })
        
        # Calculate total metrics
        total_impressions = sum(platform['impressions'] for platform in platform_metrics)
        total_clicks = sum(platform['clicks'] for platform in platform_metrics)
        total_conversions = sum(platform['conversions'] for platform in platform_metrics)
        total_spend = sum(platform['spend'] for platform in platform_metrics)
        total_revenue = sum(platform['revenue'] for platform in platform_metrics)
        
        # Calculate overall derived metrics
        overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        overall_cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
        overall_cpc = total_spend / total_clicks if total_clicks > 0 else 0
        overall_cpa = total_spend / total_conversions if total_conversions > 0 else 0
        overall_roas = total_revenue / total_spend if total_spend > 0 else 0
        
        # Find best performing platform for each metric
        best_ctr_platform = max(platform_metrics, key=lambda x: x['ctr'])
        best_cvr_platform = max(platform_metrics, key=lambda x: x['cvr'])
        best_roas_platform = max(platform_metrics, key=lambda x: x['roas'])
        
        # Generate insights
        insights = []
        
        # Overall performance insight
        insights.append({
            'id': generate_id(),
            'type': 'overall',
            'description': f"Your campaigns across all platforms have generated {total_conversions} conversions from {total_impressions} impressions, with an overall ROAS of {overall_roas:.2f}."
        })
        
        # Best performing platform insights
        insights.append({
            'id': generate_id(),
            'type': 'platform_comparison',
            'description': f"{best_ctr_platform['platform'].capitalize()} has the highest click-through rate at {best_ctr_platform['ctr']:.2f}%."
        })
        
        insights.append({
            'id': generate_id(),
            'type': 'platform_comparison',
            'description': f"{best_cvr_platform['platform'].capitalize()} has the highest conversion rate at {best_cvr_platform['cvr']:.2f}%."
        })
        
        insights.append({
            'id': generate_id(),
            'type': 'platform_comparison',
            'description': f"{best_roas_platform['platform'].capitalize()} has the highest return on ad spend at {best_roas_platform['roas']:.2f}."
        })
        
        # Budget allocation insight
        if total_spend > 0:
            # Calculate current budget allocation
            budget_allocation = []
            
            for platform in platform_metrics:
                if platform['spend'] > 0:
                    allocation_percentage = platform['spend'] / total_spend * 100
                    budget_allocation.append({
                        'platform': platform['platform'],
                        'spend': platform['spend'],
                        'allocation_percentage': allocation_percentage
                    })
            
            # Sort by allocation percentage
            budget_allocation.sort(key=lambda x: x['allocation_percentage'], reverse=True)
            
            # Generate insight
            allocation_description = ', '.join([f"{item['platform'].capitalize()}: {item['allocation_percentage']:.1f}%" for item in budget_allocation])
            
            insights.append({
                'id': generate_id(),
                'type': 'budget_allocation',
                'description': f"Current budget allocation: {allocation_description}."
            })
        
        # Optimization opportunities
        # Find platforms with below-average performance
        avg_cvr = sum(platform['cvr'] for platform in platform_metrics) / len(platform_metrics)
        
        for platform in platform_metrics:
            if platform['cvr'] < avg_cvr * 0.8:  # 20% below average
                insights.append({
                    'id': generate_id(),
                    'type': 'optimization_opportunity',
                    'description': f"{platform['platform'].capitalize()} has a conversion rate {(avg_cvr - platform['cvr']) / avg_cvr * 100:.1f}% below average. Consider optimizing this campaign or reallocating budget to better-performing platforms."
                })
        
        # Generate recommendations
        recommendations = []
        
        # Budget allocation recommendation
        optimized_budget = self._optimize_cross_platform_budget(platform_metrics)
        
        recommendations.append({
            'id': generate_id(),
            'type': 'budget',
            'priority': 'high',
            'description': 'Optimize budget allocation across platforms based on performance.',
            'expected_impact': 'Allocating more budget to high-performing platforms can improve overall ROAS.'
        })
        
        # Platform-specific recommendations
        for platform in platform_metrics:
            if platform['platform'] == 'facebook':
                recommendations.append({
                    'id': generate_id(),
                    'type': 'platform_specific',
                    'priority': 'medium',
                    'description': 'For Facebook, focus on detailed targeting and custom audiences based on your website visitors and customer lists.',
                    'expected_impact': 'Improved targeting can increase relevance and conversion rates.'
                })
            elif platform['platform'] == 'instagram':
                recommendations.append({
                    'id': generate_id(),
                    'type': 'platform_specific',
                    'priority': 'medium',
                    'description': 'For Instagram, focus on high-quality visuals and engaging stories to capture attention in a crowded feed.',
                    'expected_impact': 'Better visuals can improve engagement and click-through rates.'
                })
            elif platform['platform'] == 'tiktok':
                recommendations.append({
                    'id': generate_id(),
                    'type': 'platform_specific',
                    'priority': 'medium',
                    'description': 'For TikTok, create native-looking content that aligns with current trends and user behavior on the platform.',
                    'expected_impact': 'Native content typically performs better on TikTok.'
                })
            elif platform['platform'] == 'shopee':
                recommendations.append({
                    'id': generate_id(),
                    'type': 'platform_specific',
                    'priority': 'medium',
                    'description': 'For Shopee, optimize product listings and participate in platform promotions to increase visibility.',
                    'expected_impact': 'Improved listings and promotions can drive more sales on Shopee.'
                })
        
        # Cross-platform recommendation
        recommendations.append({
            'id': generate_id(),
            'type': 'cross_platform',
            'priority': 'high',
            'description': 'Ensure consistent messaging and branding across all platforms while adapting content format to each platform\'s unique characteristics.',
            'expected_impact': 'Consistent branding with platform-specific optimizations can improve overall campaign performance.'
        })
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'platform_metrics': platform_metrics,
            'overall_metrics': {
                'impressions': total_impressions,
                'clicks': total_clicks,
                'conversions': total_conversions,
                'spend': total_spend,
                'revenue': total_revenue,
                'ctr': overall_ctr,
                'cvr': overall_cvr,
                'cpc': overall_cpc,
                'cpa': overall_cpa,
                'roas': overall_roas
            }
        }
