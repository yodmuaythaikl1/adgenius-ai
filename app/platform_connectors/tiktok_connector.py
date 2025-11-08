"""
AdGenius AI Backend - TikTok API Connector
"""
import os
import json
import logging
import time
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

import requests

from app.models.campaign import Campaign
from app.utils.helpers import generate_id

logger = logging.getLogger(__name__)

class TikTokConnector:
    """TikTok API connector"""
    
    def __init__(self):
        """Initialize TikTok connector"""
        self.app_id = os.getenv('TIKTOK_APP_ID')
        self.app_secret = os.getenv('TIKTOK_APP_SECRET')
        self.api_base_url = os.getenv('TIKTOK_API_BASE_URL', 'https://business-api.tiktok.com/open_api/v1.3')
        self.initialized = False
    
    def initialize(self, access_token: str):
        """
        Initialize TikTok API
        
        Args:
            access_token (str): Access token
        """
        try:
            self.access_token = access_token
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize TikTok API: {str(e)}")
            self.initialized = False
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """
        Make API request to TikTok
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            params (Dict, optional): Query parameters
            data (Dict, optional): Request body
            
        Returns:
            Dict: API response
        """
        if not self.initialized:
            return {'error': 'TikTok API not initialized'}
        
        # Build URL
        url = f"{self.api_base_url}{endpoint}"
        
        # Build headers
        headers = {
            'Access-Token': self.access_token,
            'Content-Type': 'application/json'
        }
        
        # Add signature
        timestamp = str(int(time.time()))
        headers['Timestamp'] = timestamp
        
        # Generate signature
        signature_string = f"{self.app_id}{timestamp}{json.dumps(data) if data else ''}"
        signature = hmac.new(
            self.app_secret.encode(),
            signature_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        headers['Signature'] = signature
        
        try:
            # Make request
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, json=data, headers=headers)
            else:
                return {'error': f"Unsupported HTTP method: {method}"}
            
            # Parse response
            response_data = response.json()
            
            # Check for errors
            if response.status_code != 200 or response_data.get('code') != 0:
                error_message = response_data.get('message', 'Unknown error')
                logger.error(f"TikTok API error: {error_message}")
                return {'error': f"TikTok API error: {error_message}"}
            
            return response_data.get('data', {})
        except Exception as e:
            logger.error(f"Error making TikTok API request: {str(e)}")
            return {'error': f"Error making TikTok API request: {str(e)}"}
    
    def get_ad_accounts(self) -> List[Dict]:
        """
        Get ad accounts
        
        Returns:
            List[Dict]: Ad accounts
        """
        try:
            # Get advertiser IDs
            response = self._make_request('GET', '/oauth2/advertiser/get/')
            
            if 'error' in response:
                return response
            
            # Format accounts
            result = []
            
            for advertiser in response.get('list', []):
                result.append({
                    'id': advertiser.get('advertiser_id'),
                    'name': advertiser.get('advertiser_name'),
                    'status': advertiser.get('status'),
                    'currency': advertiser.get('currency'),
                    'timezone': advertiser.get('timezone')
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting ad accounts: {str(e)}")
            return {'error': f"Error getting ad accounts: {str(e)}"}
    
    def search_targeting_keywords(self, advertiser_id: str, query: str, targeting_type: str = 'interest_category') -> List[Dict]:
        """
        Search targeting keywords
        
        Args:
            advertiser_id (str): Advertiser ID
            query (str): Search query
            targeting_type (str, optional): Targeting type. Defaults to 'interest_category'.
            
        Returns:
            List[Dict]: Targeting keywords
        """
        try:
            # Map targeting type
            type_mapping = {
                'interest_category': 'INTEREST_CATEGORY',
                'behavior': 'BEHAVIOR',
                'video_interaction': 'VIDEO_INTERACTION',
                'creator_interaction': 'CREATOR_INTERACTION',
                'hashtag': 'HASHTAG'
            }
            
            tt_targeting_type = type_mapping.get(targeting_type, 'INTEREST_CATEGORY')
            
            # Search targeting
            data = {
                'advertiser_id': advertiser_id,
                'targeting_type': tt_targeting_type,
                'keyword': query,
                'limit': 100
            }
            
            response = self._make_request('POST', '/tool/interest_keyword/recommend/', data=data)
            
            if 'error' in response:
                return response
            
            # Format results
            formatted_results = []
            
            for result in response.get('list', []):
                formatted_results.append({
                    'id': result.get('id'),
                    'name': result.get('name'),
                    'type': targeting_type,
                    'audience_size': result.get('audience_size'),
                    'description': result.get('description', '')
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching targeting keywords: {str(e)}")
            return {'error': f"Error searching targeting keywords: {str(e)}"}
    
    def get_keyword_insights(self, advertiser_id: str, keywords: List[str]) -> Dict:
        """
        Get keyword insights
        
        Args:
            advertiser_id (str): Advertiser ID
            keywords (List[str]): Keywords
            
        Returns:
            Dict: Keyword insights
        """
        try:
            # Get keyword insights
            insights = {}
            
            for keyword in keywords:
                # Search for keyword
                data = {
                    'advertiser_id': advertiser_id,
                    'targeting_type': 'INTEREST_CATEGORY',
                    'keyword': keyword,
                    'limit': 10
                }
                
                response = self._make_request('POST', '/tool/interest_keyword/recommend/', data=data)
                
                if 'error' in response:
                    insights[keyword] = {
                        'found': False,
                        'audience_size': 0,
                        'related_interests': []
                    }
                    continue
                
                results = response.get('list', [])
                
                if not results:
                    insights[keyword] = {
                        'found': False,
                        'audience_size': 0,
                        'related_interests': []
                    }
                    continue
                
                # Get first result
                result = results[0]
                
                # Get related interests
                related_data = {
                    'advertiser_id': advertiser_id,
                    'targeting_type': 'INTEREST_CATEGORY',
                    'interest_ids': [result.get('id')],
                    'limit': 10
                }
                
                related_response = self._make_request('POST', '/tool/interest_action/recommend/', data=related_data)
                
                related_interests = []
                
                if 'error' not in related_response:
                    for related in related_response.get('list', []):
                        related_interests.append({
                            'id': related.get('id'),
                            'name': related.get('name'),
                            'audience_size': related.get('audience_size', 0)
                        })
                
                # Add to insights
                insights[keyword] = {
                    'found': True,
                    'id': result.get('id'),
                    'name': result.get('name'),
                    'audience_size': result.get('audience_size', 0),
                    'related_interests': related_interests
                }
            
            return insights
        except Exception as e:
            logger.error(f"Error getting keyword insights: {str(e)}")
            return {'error': f"Error getting keyword insights: {str(e)}"}
    
    def search_hashtags(self, advertiser_id: str, query: str) -> List[Dict]:
        """
        Search TikTok hashtags
        
        Args:
            advertiser_id (str): Advertiser ID
            query (str): Search query
            
        Returns:
            List[Dict]: Hashtags
        """
        try:
            # Search hashtags
            data = {
                'advertiser_id': advertiser_id,
                'targeting_type': 'HASHTAG',
                'keyword': query,
                'limit': 100
            }
            
            response = self._make_request('POST', '/tool/hashtag/recommend/', data=data)
            
            if 'error' in response:
                return response
            
            # Format results
            formatted_results = []
            
            for result in response.get('list', []):
                formatted_results.append({
                    'id': result.get('id'),
                    'name': result.get('name'),
                    'audience_size': result.get('audience_size'),
                    'video_count': result.get('video_count', 0)
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching hashtags: {str(e)}")
            return {'error': f"Error searching hashtags: {str(e)}"}
    
    def get_hashtag_insights(self, advertiser_id: str, hashtag_id: str) -> Dict:
        """
        Get hashtag insights
        
        Args:
            advertiser_id (str): Advertiser ID
            hashtag_id (str): Hashtag ID
            
        Returns:
            Dict: Hashtag insights
        """
        try:
            # Get hashtag details
            data = {
                'advertiser_id': advertiser_id,
                'hashtag_ids': [hashtag_id]
            }
            
            response = self._make_request('POST', '/tool/hashtag/info/', data=data)
            
            if 'error' in response:
                return response
            
            # Get first result
            if not response.get('list'):
                return {'error': 'Hashtag not found'}
            
            hashtag = response.get('list')[0]
            
            # Get related hashtags
            related_data = {
                'advertiser_id': advertiser_id,
                'targeting_type': 'HASHTAG',
                'hashtag_ids': [hashtag_id],
                'limit': 10
            }
            
            related_response = self._make_request('POST', '/tool/hashtag/recommend/', data=related_data)
            
            related_hashtags = []
            
            if 'error' not in related_response:
                for related in related_response.get('list', []):
                    related_hashtags.append({
                        'id': related.get('id'),
                        'name': related.get('name'),
                        'audience_size': related.get('audience_size', 0),
                        'video_count': related.get('video_count', 0)
                    })
            
            return {
                'id': hashtag.get('id'),
                'name': hashtag.get('name'),
                'audience_size': hashtag.get('audience_size', 0),
                'video_count': hashtag.get('video_count', 0),
                'related_hashtags': related_hashtags
            }
        except Exception as e:
            logger.error(f"Error getting hashtag insights: {str(e)}")
            return {'error': f"Error getting hashtag insights: {str(e)}"}
    
    def publish_campaign(self, campaign: Campaign) -> Dict:
        """
        Publish campaign to TikTok
        
        Args:
            campaign (Campaign): Campaign
            
        Returns:
            Dict: Result with platform ID
        """
        # Get user
        user = campaign.user
        
        # Find TikTok account
        tiktok_account = None
        
        for account in user.platform_accounts:
            if account.platform == 'tiktok':
                tiktok_account = account
                break
        
        if not tiktok_account:
            return {'error': 'No TikTok account found'}
        
        # Initialize API
        self.initialize(tiktok_account.access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize TikTok API'}
        
        try:
            advertiser_id = tiktok_account.account_id
            
            # Create campaign
            campaign_data = {
                'advertiser_id': advertiser_id,
                'campaign_name': campaign.name,
                'objective_type': self._map_objective(campaign.objective),
                'budget_mode': 'BUDGET_MODE_DAY' if campaign.budget.type == 'daily' else 'BUDGET_MODE_TOTAL',
                'budget': int(campaign.budget.amount * 100),  # Convert to cents
                'status': 'CAMPAIGN_STATUS_PAUSE'  # Start as paused
            }
            
            campaign_response = self._make_request('POST', '/campaign/create/', data=campaign_data)
            
            if 'error' in campaign_response:
                return campaign_response
            
            # Get campaign ID
            campaign_id = campaign_response.get('campaign_id')
            
            # Create ad group
            ad_group_data = {
                'advertiser_id': advertiser_id,
                'campaign_id': campaign_id,
                'adgroup_name': f"{campaign.name} - Ad Group",
                'placement_type': 'PLACEMENT_TYPE_NORMAL',
                'placement': ['PLACEMENT_TIKTOK'],
                'bid_type': 'BID_TYPE_CPM',
                'bid': 1000,  # $10 per 1000 impressions
                'budget_mode': 'BUDGET_MODE_DAY' if campaign.budget.type == 'daily' else 'BUDGET_MODE_TOTAL',
                'budget': int(campaign.budget.amount * 100),  # Convert to cents
                'schedule_type': 'SCHEDULE_TYPE_START_END',
                'schedule_start_time': campaign.schedule.start_date.strftime('%Y-%m-%d %H:%M:%S') if campaign.schedule else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'schedule_end_time': campaign.schedule.end_date.strftime('%Y-%m-%d %H:%M:%S') if campaign.schedule and campaign.schedule.end_date else (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'status': 'ADGROUP_STATUS_PAUSE',  # Start as paused
                'optimization_goal': self._map_optimization_goal(campaign.targeting.optimization_goal),
                'audience': self._build_targeting(campaign.targeting)
            }
            
            ad_group_response = self._make_request('POST', '/adgroup/create/', data=ad_group_data)
            
            if 'error' in ad_group_response:
                return ad_group_response
            
            # Get ad group ID
            ad_group_id = ad_group_response.get('adgroup_id')
            
            # Create ads for each creative
            ad_ids = []
            
            for creative in campaign.creatives:
                # Upload image
                image_id = None
                
                if creative.media_urls:
                    image_id = self._upload_image(advertiser_id, creative.media_urls[0])
                    
                    if isinstance(image_id, dict) and 'error' in image_id:
                        return image_id
                
                # Create ad
                ad_data = {
                    'advertiser_id': advertiser_id,
                    'adgroup_id': ad_group_id,
                    'ad_name': f"{campaign.name} - {creative.name}",
                    'status': 'AD_STATUS_PAUSE',  # Start as paused
                    'creative_info': {
                        'creative_type': 'SINGLE_IMAGE' if image_id else 'SINGLE_VIDEO',
                        'call_to_action': self._map_call_to_action(creative.call_to_action),
                        'image_info': {
                            'image_id': image_id
                        } if image_id else None,
                        'video_info': {
                            'video_id': self._upload_video(advertiser_id, creative.media_urls[0]) if not image_id and creative.media_urls else None
                        } if not image_id and creative.media_urls else None,
                        'ad_text': creative.primary_text,
                        'landing_page_url': creative.destination_url
                    }
                }
                
                ad_response = self._make_request('POST', '/ad/create/', data=ad_data)
                
                if 'error' in ad_response:
                    return ad_response
                
                # Get ad ID
                ad_id = ad_response.get('ad_id')
                ad_ids.append(ad_id)
                
                # Update creative with platform ID
                creative.platform_creative_id = ad_id
            
            # Save campaign
            campaign.platform_campaign_id = campaign_id
            campaign.save()
            
            return {
                'platform_id': campaign_id,
                'ad_group_id': ad_group_id,
                'ad_ids': ad_ids
            }
        except Exception as e:
            logger.error(f"Error publishing campaign: {str(e)}")
            return {'error': f"Error publishing campaign: {str(e)}"}
    
    def pause_campaign(self, advertiser_id: str, campaign_id: str) -> bool:
        """
        Pause TikTok campaign
        
        Args:
            advertiser_id (str): Advertiser ID
            campaign_id (str): Campaign ID
            
        Returns:
            bool: True if paused, False otherwise
        """
        try:
            # Pause campaign
            data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'operation_status': 'CAMPAIGN_STATUS_PAUSE'
            }
            
            response = self._make_request('POST', '/campaign/status/update/', data=data)
            
            if 'error' in response:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error pausing campaign: {str(e)}")
            return False
    
    def resume_campaign(self, advertiser_id: str, campaign_id: str) -> bool:
        """
        Resume TikTok campaign
        
        Args:
            advertiser_id (str): Advertiser ID
            campaign_id (str): Campaign ID
            
        Returns:
            bool: True if resumed, False otherwise
        """
        try:
            # Resume campaign
            data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'operation_status': 'CAMPAIGN_STATUS_NORMAL'
            }
            
            response = self._make_request('POST', '/campaign/status/update/', data=data)
            
            if 'error' in response:
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error resuming campaign: {str(e)}")
            return False
    
    def get_campaign_analytics(self, advertiser_id: str, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get campaign analytics
        
        Args:
            advertiser_id (str): Advertiser ID
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analytics
        """
        try:
            # Format dates
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Get campaign insights
            data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'fields': [
                    'campaign_id',
                    'campaign_name',
                    'impressions',
                    'clicks',
                    'cost',
                    'ctr',
                    'cpc',
                    'cpm',
                    'conversion',
                    'conversion_rate',
                    'cost_per_conversion',
                    'reach',
                    'frequency',
                    'video_play_actions',
                    'video_watched_2s',
                    'video_watched_6s',
                    'video_views_p25',
                    'video_views_p50',
                    'video_views_p75',
                    'video_views_p100'
                ],
                'data_level': 'AUCTION_CAMPAIGN',
                'report_type': 'BASIC'
            }
            
            response = self._make_request('POST', '/report/integrated/get/', data=data)
            
            if 'error' in response:
                return response
            
            # Process insights
            if not response.get('list'):
                return {'error': 'No campaign data found'}
            
            campaign_data = response.get('list')[0]
            
            # Get daily breakdown
            daily_data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'fields': [
                    'campaign_id',
                    'stat_time_day',
                    'impressions',
                    'clicks',
                    'cost',
                    'ctr',
                    'cpc',
                    'cpm',
                    'conversion',
                    'conversion_rate',
                    'cost_per_conversion',
                    'reach',
                    'frequency'
                ],
                'data_level': 'AUCTION_CAMPAIGN',
                'report_type': 'BASIC',
                'dimensions': ['stat_time_day']
            }
            
            daily_response = self._make_request('POST', '/report/integrated/get/', data=daily_data)
            
            daily_metrics = []
            
            if 'error' not in daily_response:
                for day_data in daily_response.get('list', []):
                    # Parse date
                    date = datetime.strptime(day_data.get('stat_time_day'), '%Y-%m-%d')
                    
                    daily_metrics.append({
                        'date': date.isoformat(),
                        'impressions': int(day_data.get('impressions', 0)),
                        'clicks': int(day_data.get('clicks', 0)),
                        'conversions': int(day_data.get('conversion', 0)),
                        'spend': float(day_data.get('cost', 0)) / 100,  # Convert from cents
                        'ctr': float(day_data.get('ctr', 0)) * 100,
                        'cpc': float(day_data.get('cpc', 0)) / 100,  # Convert from cents
                        'cpm': float(day_data.get('cpm', 0)) / 100,  # Convert from cents
                        'reach': int(day_data.get('reach', 0)),
                        'frequency': float(day_data.get('frequency', 0))
                    })
            
            # Get ad group insights
            ad_group_data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'fields': [
                    'adgroup_id',
                    'adgroup_name',
                    'impressions',
                    'clicks',
                    'cost',
                    'ctr',
                    'cpc',
                    'cpm',
                    'conversion',
                    'conversion_rate',
                    'cost_per_conversion'
                ],
                'data_level': 'AUCTION_ADGROUP',
                'report_type': 'BASIC'
            }
            
            ad_group_response = self._make_request('POST', '/report/integrated/get/', data=ad_group_data)
            
            ad_group_insights = []
            
            if 'error' not in ad_group_response:
                for ad_group in ad_group_response.get('list', []):
                    ad_group_insights.append({
                        'id': ad_group.get('adgroup_id'),
                        'name': ad_group.get('adgroup_name'),
                        'impressions': int(ad_group.get('impressions', 0)),
                        'clicks': int(ad_group.get('clicks', 0)),
                        'conversions': int(ad_group.get('conversion', 0)),
                        'spend': float(ad_group.get('cost', 0)) / 100,  # Convert from cents
                        'ctr': float(ad_group.get('ctr', 0)) * 100,
                        'cpc': float(ad_group.get('cpc', 0)) / 100,  # Convert from cents
                        'cpm': float(ad_group.get('cpm', 0)) / 100,  # Convert from cents
                        'conversion_rate': float(ad_group.get('conversion_rate', 0)) * 100,
                        'cost_per_conversion': float(ad_group.get('cost_per_conversion', 0)) / 100  # Convert from cents
                    })
            
            # Get ad insights
            ad_data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'fields': [
                    'ad_id',
                    'ad_name',
                    'impressions',
                    'clicks',
                    'cost',
                    'ctr',
                    'cpc',
                    'cpm',
                    'conversion',
                    'conversion_rate',
                    'cost_per_conversion',
                    'video_play_actions',
                    'video_watched_2s',
                    'video_watched_6s',
                    'video_views_p25',
                    'video_views_p50',
                    'video_views_p75',
                    'video_views_p100'
                ],
                'data_level': 'AUCTION_AD',
                'report_type': 'BASIC'
            }
            
            ad_response = self._make_request('POST', '/report/integrated/get/', data=ad_data)
            
            creative_performance = []
            
            if 'error' not in ad_response:
                for ad in ad_response.get('list', []):
                    creative_performance.append({
                        'creative_id': ad.get('ad_id'),
                        'name': ad.get('ad_name'),
                        'impressions': int(ad.get('impressions', 0)),
                        'clicks': int(ad.get('clicks', 0)),
                        'conversions': int(ad.get('conversion', 0)),
                        'spend': float(ad.get('cost', 0)) / 100,  # Convert from cents
                        'ctr': float(ad.get('ctr', 0)) * 100,
                        'cpc': float(ad.get('cpc', 0)) / 100,  # Convert from cents
                        'cpm': float(ad.get('cpm', 0)) / 100,  # Convert from cents
                        'conversion_rate': float(ad.get('conversion_rate', 0)) * 100,
                        'cost_per_conversion': float(ad.get('cost_per_conversion', 0)) / 100,  # Convert from cents
                        'video_play_actions': int(ad.get('video_play_actions', 0)),
                        'video_watched_2s': int(ad.get('video_watched_2s', 0)),
                        'video_watched_6s': int(ad.get('video_watched_6s', 0)),
                        'video_views_p25': int(ad.get('video_views_p25', 0)),
                        'video_views_p50': int(ad.get('video_views_p50', 0)),
                        'video_views_p75': int(ad.get('video_views_p75', 0)),
                        'video_views_p100': int(ad.get('video_views_p100', 0))
                    })
            
            # Get audience insights
            audience_data = {
                'advertiser_id': advertiser_id,
                'campaign_ids': [campaign_id],
                'start_date': start_date_str,
                'end_date': end_date_str,
                'fields': [
                    'gender',
                    'age',
                    'impressions',
                    'clicks',
                    'conversion',
                    'cost'
                ],
                'data_level': 'AUCTION_CAMPAIGN',
                'report_type': 'AUDIENCE',
                'dimensions': ['gender', 'age']
            }
            
            audience_response = self._make_request('POST', '/report/audience/get/', data=audience_data)
            
            audience_insights = {
                'age_gender': {},
                'locations': {},
                'interests': {},
                'behaviors': {}
            }
            
            if 'error' not in audience_response:
                for audience in audience_response.get('list', []):
                    gender = audience.get('gender', 'unknown')
                    age = audience.get('age', 'unknown')
                    key = f"{age} - {gender}"
                    
                    audience_insights['age_gender'][key] = {
                        'impressions': int(audience.get('impressions', 0)),
                        'clicks': int(audience.get('clicks', 0)),
                        'conversions': int(audience.get('conversion', 0)),
                        'spend': float(audience.get('cost', 0)) / 100  # Convert from cents
                    }
            
            # Calculate metrics
            total_impressions = int(campaign_data.get('impressions', 0))
            total_clicks = int(campaign_data.get('clicks', 0))
            total_conversions = int(campaign_data.get('conversion', 0))
            total_spend = float(campaign_data.get('cost', 0)) / 100  # Convert from cents
            
            average_ctr = float(campaign_data.get('ctr', 0)) * 100
            average_cpc = float(campaign_data.get('cpc', 0)) / 100  # Convert from cents
            average_cpm = float(campaign_data.get('cpm', 0)) / 100  # Convert from cents
            average_conversion_rate = float(campaign_data.get('conversion_rate', 0)) * 100
            average_cost_per_conversion = float(campaign_data.get('cost_per_conversion', 0)) / 100  # Convert from cents
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                total_impressions=total_impressions,
                total_clicks=total_clicks,
                total_conversions=total_conversions,
                total_spend=total_spend,
                average_ctr=average_ctr,
                average_cpc=average_cpc,
                average_conversion_rate=average_conversion_rate,
                creative_performance=creative_performance
            )
            
            return {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'total_spend': total_spend,
                'average_ctr': average_ctr,
                'average_cpc': average_cpc,
                'average_cpm': average_cpm,
                'average_conversion_rate': average_conversion_rate,
                'average_cost_per_conversion': average_cost_per_conversion,
                'daily_metrics': daily_metrics,
                'audience_insights': audience_insights,
                'creative_performance': creative_performance,
                'recommendations': recommendations,
                'video_metrics': {
                    'video_play_actions': int(campaign_data.get('video_play_actions', 0)),
                    'video_watched_2s': int(campaign_data.get('video_watched_2s', 0)),
                    'video_watched_6s': int(campaign_data.get('video_watched_6s', 0)),
                    'video_views_p25': int(campaign_data.get('video_views_p25', 0)),
                    'video_views_p50': int(campaign_data.get('video_views_p50', 0)),
                    'video_views_p75': int(campaign_data.get('video_views_p75', 0)),
                    'video_views_p100': int(campaign_data.get('video_views_p100', 0))
                }
            }
        except Exception as e:
            logger.error(f"Error getting campaign analytics: {str(e)}")
            return {'error': f"Error getting campaign analytics: {str(e)}"}
    
    def _map_objective(self, objective: str) -> str:
        """
        Map campaign objective
        
        Args:
            objective (str): Campaign objective
            
        Returns:
            str: TikTok campaign objective
        """
        objective_mapping = {
            'awareness': 'REACH',
            'consideration': 'TRAFFIC',
            'conversion': 'CONVERSIONS'
        }
        
        return objective_mapping.get(objective, 'REACH')
    
    def _map_optimization_goal(self, optimization_goal: str) -> str:
        """
        Map optimization goal
        
        Args:
            optimization_goal (str): Optimization goal
            
        Returns:
            str: TikTok optimization goal
        """
        goal_mapping = {
            'REACH': 'REACH',
            'IMPRESSIONS': 'IMPRESSION',
            'LINK_CLICKS': 'CLICK',
            'CONVERSIONS': 'CONVERSION',
            'APP_INSTALLS': 'INSTALL',
            'VIDEO_VIEWS': 'VIDEO_VIEW'
        }
        
        return goal_mapping.get(optimization_goal, 'REACH')
    
    def _map_call_to_action(self, call_to_action: str) -> str:
        """
        Map call to action
        
        Args:
            call_to_action (str): Call to action
            
        Returns:
            str: TikTok call to action
        """
        cta_mapping = {
            'shop_now': 'SHOP_NOW',
            'book_now': 'BOOK_NOW',
            'learn_more': 'LEARN_MORE',
            'sign_up': 'SIGN_UP',
            'download': 'DOWNLOAD_NOW',
            'watch_more': 'WATCH_MORE',
            'contact_us': 'CONTACT',
            'apply_now': 'APPLY_NOW',
            'buy_now': 'BUY_NOW'
        }
        
        return cta_mapping.get(call_to_action, 'LEARN_MORE')
    
    def _build_targeting(self, targeting) -> Dict:
        """
        Build targeting object
        
        Args:
            targeting: Targeting model
            
        Returns:
            Dict: TikTok targeting object
        """
        tt_targeting = {}
        
        # Age range
        if targeting.age_min or targeting.age_max:
            age_groups = []
            
            age_mapping = {
                (13, 17): 'AGE_13_17',
                (18, 24): 'AGE_18_24',
                (25, 34): 'AGE_25_34',
                (35, 44): 'AGE_35_44',
                (45, 54): 'AGE_45_54',
                (55, 100): 'AGE_55_100'
            }
            
            for (min_age, max_age), age_group in age_mapping.items():
                if (not targeting.age_min or min_age >= targeting.age_min) and (not targeting.age_max or max_age <= targeting.age_max):
                    age_groups.append(age_group)
            
            if age_groups:
                tt_targeting['age'] = age_groups
        
        # Genders
        if targeting.genders:
            gender_mapping = {
                'male': 'GENDER_MALE',
                'female': 'GENDER_FEMALE',
                'all': None
            }
            
            genders = []
            
            for gender in targeting.genders:
                if gender in gender_mapping and gender_mapping[gender]:
                    genders.append(gender_mapping[gender])
            
            if genders:
                tt_targeting['gender'] = genders
        
        # Locations
        if targeting.locations:
            countries = []
            regions = []
            cities = []
            
            for location in targeting.locations:
                location_type = location.get('type')
                
                if location_type == 'country':
                    countries.append(location.get('key'))
                elif location_type == 'region':
                    regions.append({
                        'region_id': location.get('key'),
                        'country_code': location.get('country')
                    })
                elif location_type == 'city':
                    cities.append({
                        'city_id': location.get('key'),
                        'region_id': location.get('region'),
                        'country_code': location.get('country')
                    })
            
            if countries:
                tt_targeting['location'] = {
                    'type': 'LOCATION_TYPE_COUNTRY',
                    'ids': countries
                }
            elif regions:
                tt_targeting['location'] = {
                    'type': 'LOCATION_TYPE_REGION',
                    'ids': [region['region_id'] for region in regions]
                }
            elif cities:
                tt_targeting['location'] = {
                    'type': 'LOCATION_TYPE_CITY',
                    'ids': [city['city_id'] for city in cities]
                }
        
        # Interests
        if targeting.interests:
            tt_targeting['interest_category_ids'] = []
            
            for interest in targeting.interests:
                tt_targeting['interest_category_ids'].append(interest.get('id'))
        
        # Behaviors
        if targeting.behaviors:
            tt_targeting['behavior_ids'] = []
            
            for behavior in targeting.behaviors:
                tt_targeting['behavior_ids'].append(behavior.get('id'))
        
        # Device platforms
        if targeting.device_platforms:
            platform_mapping = {
                'mobile': 'MOBILE',
                'desktop': 'PC',
                'all': None
            }
            
            platforms = []
            
            for platform in targeting.device_platforms:
                if platform in platform_mapping and platform_mapping[platform]:
                    platforms.append(platform_mapping[platform])
            
            if platforms:
                tt_targeting['device_model_ids'] = platforms
        
        # Operating systems
        if targeting.operating_systems:
            os_mapping = {
                'android': 'ANDROID',
                'ios': 'IOS',
                'all': None
            }
            
            os_list = []
            
            for os in targeting.operating_systems:
                if os in os_mapping and os_mapping[os]:
                    os_list.append(os_mapping[os])
            
            if os_list:
                tt_targeting['os_ids'] = os_list
        
        # Network types
        if targeting.network_types:
            network_mapping = {
                'wifi': 'NETWORK_WIFI',
                'cellular': 'NETWORK_MOBILE',
                'all': None
            }
            
            networks = []
            
            for network in targeting.network_types:
                if network in network_mapping and network_mapping[network]:
                    networks.append(network_mapping[network])
            
            if networks:
                tt_targeting['connection_type_ids'] = networks
        
        return tt_targeting
    
    def _upload_image(self, advertiser_id: str, image_url: str) -> str:
        """
        Upload image to TikTok
        
        Args:
            advertiser_id (str): Advertiser ID
            image_url (str): Image URL
            
        Returns:
            str: Image ID
        """
        try:
            # Download image
            response = requests.get(image_url)
            
            if response.status_code != 200:
                return {'error': f"Failed to download image: {response.status_code}"}
            
            # Get file content
            file_content = response.content
            
            # Upload image
            files = {
                'image_file': ('image.jpg', file_content, 'image/jpeg')
            }
            
            # Build URL
            url = f"{self.api_base_url}/file/image/ad/upload/"
            
            # Build headers
            headers = {
                'Access-Token': self.access_token
            }
            
            # Add signature
            timestamp = str(int(time.time()))
            headers['Timestamp'] = timestamp
            
            # Generate signature
            signature_string = f"{self.app_id}{timestamp}"
            signature = hmac.new(
                self.app_secret.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers['Signature'] = signature
            
            # Make request
            response = requests.post(
                url,
                files=files,
                data={'advertiser_id': advertiser_id},
                headers=headers
            )
            
            # Parse response
            response_data = response.json()
            
            # Check for errors
            if response.status_code != 200 or response_data.get('code') != 0:
                error_message = response_data.get('message', 'Unknown error')
                logger.error(f"TikTok API error: {error_message}")
                return {'error': f"TikTok API error: {error_message}"}
            
            # Get image ID
            return response_data.get('data', {}).get('image_id')
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return {'error': f"Error uploading image: {str(e)}"}
    
    def _upload_video(self, advertiser_id: str, video_url: str) -> str:
        """
        Upload video to TikTok
        
        Args:
            advertiser_id (str): Advertiser ID
            video_url (str): Video URL
            
        Returns:
            str: Video ID
        """
        try:
            # Download video
            response = requests.get(video_url)
            
            if response.status_code != 200:
                return {'error': f"Failed to download video: {response.status_code}"}
            
            # Get file content
            file_content = response.content
            
            # Upload video
            files = {
                'video_file': ('video.mp4', file_content, 'video/mp4')
            }
            
            # Build URL
            url = f"{self.api_base_url}/file/video/ad/upload/"
            
            # Build headers
            headers = {
                'Access-Token': self.access_token
            }
            
            # Add signature
            timestamp = str(int(time.time()))
            headers['Timestamp'] = timestamp
            
            # Generate signature
            signature_string = f"{self.app_id}{timestamp}"
            signature = hmac.new(
                self.app_secret.encode(),
                signature_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            headers['Signature'] = signature
            
            # Make request
            response = requests.post(
                url,
                files=files,
                data={'advertiser_id': advertiser_id},
                headers=headers
            )
            
            # Parse response
            response_data = response.json()
            
            # Check for errors
            if response.status_code != 200 or response_data.get('code') != 0:
                error_message = response_data.get('message', 'Unknown error')
                logger.error(f"TikTok API error: {error_message}")
                return {'error': f"TikTok API error: {error_message}"}
            
            # Get video ID
            return response_data.get('data', {}).get('video_id')
        except Exception as e:
            logger.error(f"Error uploading video: {str(e)}")
            return {'error': f"Error uploading video: {str(e)}"}
    
    def _generate_recommendations(self, total_impressions: int, total_clicks: int, 
                                total_conversions: int, total_spend: float, 
                                average_ctr: float, average_cpc: float, 
                                average_conversion_rate: float, 
                                creative_performance: List[Dict]) -> List[Dict]:
        """
        Generate recommendations
        
        Args:
            total_impressions (int): Total impressions
            total_clicks (int): Total clicks
            total_conversions (int): Total conversions
            total_spend (float): Total spend
            average_ctr (float): Average CTR
            average_cpc (float): Average CPC
            average_conversion_rate (float): Average conversion rate
            creative_performance (List[Dict]): Creative performance
            
        Returns:
            List[Dict]: Recommendations
        """
        recommendations = []
        
        # Check CTR
        if average_ctr < 1.5:  # TikTok typically has higher CTR than other platforms
            recommendations.append({
                'id': generate_id(),
                'type': 'creative',
                'priority': 'high',
                'description': 'Your click-through rate (CTR) is below average for TikTok. Consider using more engaging videos with trending sounds or effects.',
                'expected_impact': 'Increasing CTR can lead to more clicks and potentially more conversions.'
            })
        
        # Check CPC
        if average_cpc > 1.0:  # TikTok typically has lower CPC than other platforms
            recommendations.append({
                'id': generate_id(),
                'type': 'targeting',
                'priority': 'medium',
                'description': 'Your cost per click (CPC) is high for TikTok. Consider refining your targeting to reach a more relevant audience.',
                'expected_impact': 'Reducing CPC can help you get more clicks for your budget.'
            })
        
        # Check conversion rate
        if average_conversion_rate < 2.0:  # TikTok typically has higher conversion rates for certain verticals
            recommendations.append({
                'id': generate_id(),
                'type': 'landing_page',
                'priority': 'high',
                'description': 'Your conversion rate is low. Consider improving your landing page experience or ensuring your offer is compelling.',
                'expected_impact': 'Increasing conversion rate directly impacts your return on ad spend.'
            })
        
        # TikTok-specific recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'medium',
            'description': 'Consider using TikTok-native content formats like challenges or trending sounds to increase engagement.',
            'expected_impact': 'Native content typically performs better on TikTok.'
        })
        
        recommendations.append({
            'id': generate_id(),
            'type': 'targeting',
            'priority': 'low',
            'description': 'Use hashtag targeting to reach users interested in specific topics related to your product.',
            'expected_impact': 'Hashtag targeting can help reach more relevant audiences.'
        })
        
        # Check video metrics
        if creative_performance:
            # Find videos with low completion rates
            low_completion_videos = []
            
            for creative in creative_performance:
                if 'video_views_p100' in creative and 'video_play_actions' in creative:
                    completion_rate = creative['video_views_p100'] / creative['video_play_actions'] if creative['video_play_actions'] > 0 else 0
                    
                    if completion_rate < 0.2:  # Less than 20% completion rate
                        low_completion_videos.append(creative['name'])
            
            if low_completion_videos:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'creative',
                    'priority': 'high',
                    'description': f"The following videos have low completion rates: {', '.join(low_completion_videos)}. Consider creating shorter, more engaging videos.",
                    'expected_impact': 'Higher video completion rates typically lead to better performance.'
                })
        
        # Check creative performance
        if creative_performance and len(creative_performance) > 1:
            # Find best and worst performing creatives
            best_creative = max(creative_performance, key=lambda x: x.get('ctr', 0))
            worst_creative = min(creative_performance, key=lambda x: x.get('ctr', 0))
            
            # If there's a significant difference
            if best_creative.get('ctr', 0) > worst_creative.get('ctr', 0) * 2:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'creative',
                    'priority': 'medium',
                    'description': f"There's a significant performance gap between your creatives. Consider pausing the low-performing creative and creating a new one based on what works in your high-performing creative.",
                    'expected_impact': 'Focusing budget on high-performing creatives can improve overall campaign performance.'
                })
        
        return recommendations
