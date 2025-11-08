"""
AdGenius AI Backend - Facebook API Connector
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign as FBCampaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.targetingsearch import TargetingSearch
from facebook_business.adobjects.targeting import Targeting
from facebook_business.exceptions import FacebookRequestError

from app.models.campaign import Campaign
from app.utils.helpers import generate_id

logger = logging.getLogger(__name__)

class FacebookConnector:
    """Facebook API connector"""
    
    def __init__(self):
        """Initialize Facebook connector"""
        self.app_id = os.getenv('FACEBOOK_APP_ID')
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.api_version = os.getenv('FACEBOOK_API_VERSION', 'v16.0')
        self.initialized = False
    
    def initialize(self, access_token: str):
        """
        Initialize Facebook Ads API
        
        Args:
            access_token (str): Access token
        """
        try:
            FacebookAdsApi.init(self.app_id, self.app_secret, access_token, api_version=self.api_version)
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Facebook Ads API: {str(e)}")
            self.initialized = False
    
    def get_ad_accounts(self, access_token: str) -> List[Dict]:
        """
        Get ad accounts
        
        Args:
            access_token (str): Access token
            
        Returns:
            List[Dict]: Ad accounts
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Facebook Ads API'}
        
        try:
            # Get ad accounts
            from facebook_business.adobjects.user import User
            me = User(fbid='me')
            accounts = me.get_ad_accounts(fields=['id', 'name', 'account_status', 'currency', 'business_name'])
            
            # Format accounts
            result = []
            
            for account in accounts:
                result.append({
                    'id': account['id'],
                    'name': account['name'],
                    'status': 'active' if account.get('account_status') == 1 else 'inactive',
                    'currency': account.get('currency'),
                    'business_name': account.get('business_name')
                })
            
            return result
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return {'error': f"Facebook API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting ad accounts: {str(e)}")
            return {'error': f"Error getting ad accounts: {str(e)}"}
    
    def search_targeting_keywords(self, access_token: str, query: str, targeting_type: str = 'interests') -> List[Dict]:
        """
        Search targeting keywords
        
        Args:
            access_token (str): Access token
            query (str): Search query
            targeting_type (str, optional): Targeting type. Defaults to 'interests'.
            
        Returns:
            List[Dict]: Targeting keywords
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Facebook Ads API'}
        
        try:
            # Map targeting type
            type_mapping = {
                'interests': 'adinterest',
                'behaviors': 'behavior',
                'demographics': 'demographic',
                'life_events': 'life_event',
                'industries': 'industry',
                'income': 'income',
                'family_statuses': 'family_status',
                'education_statuses': 'education_status'
            }
            
            fb_targeting_type = type_mapping.get(targeting_type, 'adinterest')
            
            # Search targeting
            params = {
                'q': query,
                'type': fb_targeting_type,
                'limit': 100
            }
            
            results = TargetingSearch.search(params=params)
            
            # Format results
            formatted_results = []
            
            for result in results:
                formatted_results.append({
                    'id': result.get('id'),
                    'name': result.get('name'),
                    'type': targeting_type,
                    'path': result.get('path', []),
                    'audience_size': result.get('audience_size'),
                    'description': result.get('description', '')
                })
            
            return formatted_results
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return {'error': f"Facebook API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error searching targeting keywords: {str(e)}")
            return {'error': f"Error searching targeting keywords: {str(e)}"}
    
    def get_keyword_insights(self, access_token: str, ad_account_id: str, keywords: List[str]) -> Dict:
        """
        Get keyword insights
        
        Args:
            access_token (str): Access token
            ad_account_id (str): Ad account ID
            keywords (List[str]): Keywords
            
        Returns:
            Dict: Keyword insights
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Facebook Ads API'}
        
        try:
            # Get ad account
            account = AdAccount(ad_account_id)
            
            # Get keyword insights
            insights = {}
            
            for keyword in keywords:
                # Search for keyword
                params = {
                    'q': keyword,
                    'type': 'adinterest',
                    'limit': 10
                }
                
                results = TargetingSearch.search(params=params)
                
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
                related_params = {
                    'type': 'adinterestsuggestion',
                    'interest_list': [result.get('id')],
                    'limit': 10
                }
                
                related_results = TargetingSearch.search(params=related_params)
                
                related_interests = []
                
                for related in related_results:
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
                    'path': result.get('path', []),
                    'related_interests': related_interests
                }
            
            return insights
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return {'error': f"Facebook API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting keyword insights: {str(e)}")
            return {'error': f"Error getting keyword insights: {str(e)}"}
    
    def publish_campaign(self, campaign: Campaign) -> Dict:
        """
        Publish campaign to Facebook
        
        Args:
            campaign (Campaign): Campaign
            
        Returns:
            Dict: Result with platform ID
        """
        # Get user
        user = campaign.user
        
        # Find Facebook account
        facebook_account = None
        
        for account in user.platform_accounts:
            if account.platform == 'facebook':
                facebook_account = account
                break
        
        if not facebook_account:
            return {'error': 'No Facebook account found'}
        
        # Initialize API
        self.initialize(facebook_account.access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Facebook Ads API'}
        
        try:
            # Get ad account
            account = AdAccount(facebook_account.account_id)
            
            # Create campaign
            fb_campaign = account.create_campaign(
                params={
                    'name': campaign.name,
                    'objective': self._map_objective(campaign.objective),
                    'status': 'PAUSED',  # Start as paused
                    'special_ad_categories': []
                }
            )
            
            # Get campaign ID
            campaign_id = fb_campaign['id']
            
            # Create ad set
            targeting = self._build_targeting(campaign.targeting)
            
            ad_set = account.create_ad_set(
                params={
                    'name': f"{campaign.name} - Ad Set",
                    'campaign_id': campaign_id,
                    'daily_budget': int(campaign.budget.amount * 100) if campaign.budget.type == 'daily' else None,
                    'lifetime_budget': int(campaign.budget.amount * 100) if campaign.budget.type == 'lifetime' else None,
                    'bid_amount': 1000,  # $10 per 1000 impressions
                    'billing_event': 'IMPRESSIONS',
                    'optimization_goal': self._map_optimization_goal(campaign.targeting.optimization_goal),
                    'targeting': targeting,
                    'status': 'PAUSED',
                    'start_time': campaign.schedule.start_date.strftime('%Y-%m-%dT%H:%M:%S%z') if campaign.schedule else None,
                    'end_time': campaign.schedule.end_date.strftime('%Y-%m-%dT%H:%M:%S%z') if campaign.schedule and campaign.schedule.end_date else None
                }
            )
            
            # Get ad set ID
            ad_set_id = ad_set['id']
            
            # Create ads for each creative
            ad_ids = []
            
            for creative in campaign.creatives:
                # Create ad creative
                ad_creative = account.create_ad_creative(
                    params={
                        'name': creative.name,
                        'object_story_spec': {
                            'page_id': facebook_account.meta_data.get('page_id'),
                            'link_data': {
                                'message': creative.primary_text,
                                'link': creative.destination_url,
                                'caption': creative.description,
                                'description': creative.description,
                                'call_to_action': {
                                    'type': self._map_call_to_action(creative.call_to_action)
                                },
                                'image_hash': self._upload_image(account, creative.media_urls[0]) if creative.media_urls else None
                            }
                        }
                    }
                )
                
                # Get creative ID
                creative_id = ad_creative['id']
                
                # Create ad
                ad = account.create_ad(
                    params={
                        'name': f"{campaign.name} - {creative.name}",
                        'adset_id': ad_set_id,
                        'creative': {'creative_id': creative_id},
                        'status': 'PAUSED'
                    }
                )
                
                # Get ad ID
                ad_id = ad['id']
                ad_ids.append(ad_id)
                
                # Update creative with platform ID
                creative.platform_creative_id = creative_id
            
            # Save campaign
            campaign.platform_campaign_id = campaign_id
            campaign.save()
            
            return {
                'platform_id': campaign_id,
                'ad_set_id': ad_set_id,
                'ad_ids': ad_ids
            }
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return {'error': f"Facebook API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error publishing campaign: {str(e)}")
            return {'error': f"Error publishing campaign: {str(e)}"}
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """
        Pause Facebook campaign
        
        Args:
            campaign_id (str): Campaign ID
            
        Returns:
            bool: True if paused, False otherwise
        """
        try:
            # Get campaign
            fb_campaign = FBCampaign(campaign_id)
            
            # Pause campaign
            fb_campaign.api_update(
                params={
                    'status': 'PAUSED'
                }
            )
            
            return True
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error pausing campaign: {str(e)}")
            return False
    
    def resume_campaign(self, campaign_id: str) -> bool:
        """
        Resume Facebook campaign
        
        Args:
            campaign_id (str): Campaign ID
            
        Returns:
            bool: True if resumed, False otherwise
        """
        try:
            # Get campaign
            fb_campaign = FBCampaign(campaign_id)
            
            # Resume campaign
            fb_campaign.api_update(
                params={
                    'status': 'ACTIVE'
                }
            )
            
            return True
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error resuming campaign: {str(e)}")
            return False
    
    def get_campaign_analytics(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get campaign analytics
        
        Args:
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analytics
        """
        try:
            # Get campaign
            fb_campaign = FBCampaign(campaign_id)
            
            # Format dates
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Get insights
            insights = fb_campaign.get_insights(
                fields=[
                    'impressions',
                    'clicks',
                    'spend',
                    'ctr',
                    'cpc',
                    'cpm',
                    'actions',
                    'conversions',
                    'conversion_values',
                    'reach',
                    'frequency'
                ],
                params={
                    'time_range': {
                        'since': start_date_str,
                        'until': end_date_str
                    },
                    'time_increment': 1  # Daily breakdown
                }
            )
            
            # Process insights
            total_impressions = 0
            total_clicks = 0
            total_spend = 0.0
            total_conversions = 0
            total_revenue = 0.0
            daily_metrics = []
            
            for insight in insights:
                # Get date
                date = datetime.strptime(insight.get('date_start'), '%Y-%m-%d')
                
                # Get basic metrics
                impressions = int(insight.get('impressions', 0))
                clicks = int(insight.get('clicks', 0))
                spend = float(insight.get('spend', 0))
                
                # Get conversions and revenue
                conversions = 0
                revenue = 0.0
                
                if 'actions' in insight:
                    for action in insight['actions']:
                        if action['action_type'] in ['purchase', 'offsite_conversion.fb_pixel_purchase']:
                            conversions += int(action.get('value', 0))
                
                if 'conversion_values' in insight:
                    for value in insight['conversion_values']:
                        if value['action_type'] in ['purchase', 'offsite_conversion.fb_pixel_purchase']:
                            revenue += float(value.get('value', 0))
                
                # Add to totals
                total_impressions += impressions
                total_clicks += clicks
                total_spend += spend
                total_conversions += conversions
                total_revenue += revenue
                
                # Add daily metric
                daily_metrics.append({
                    'date': date.isoformat(),
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'spend': spend,
                    'revenue': revenue,
                    'ctr': float(insight.get('ctr', 0)) * 100,
                    'cpc': float(insight.get('cpc', 0)),
                    'cpm': float(insight.get('cpm', 0)),
                    'reach': int(insight.get('reach', 0)),
                    'frequency': float(insight.get('frequency', 0))
                })
            
            # Calculate averages
            average_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
            average_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
            average_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
            average_conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
            average_cost_per_conversion = (total_spend / total_conversions) if total_conversions > 0 else 0
            roas = (total_revenue / total_spend) if total_spend > 0 else 0
            
            # Get ad sets
            ad_sets = fb_campaign.get_ad_sets(
                fields=[
                    'id',
                    'name',
                    'targeting'
                ]
            )
            
            # Get audience insights
            audience_insights = self._get_audience_insights(ad_sets)
            
            # Get ads
            ads = []
            
            for ad_set in ad_sets:
                ad_set_ads = ad_set.get_ads(
                    fields=[
                        'id',
                        'name',
                        'creative'
                    ]
                )
                
                ads.extend(ad_set_ads)
            
            # Get creative performance
            creative_performance = self._get_creative_performance(ads, start_date_str, end_date_str)
            
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
                'total_revenue': total_revenue,
                'average_ctr': average_ctr,
                'average_cpc': average_cpc,
                'average_cpm': average_cpm,
                'average_conversion_rate': average_conversion_rate,
                'average_cost_per_conversion': average_cost_per_conversion,
                'roas': roas,
                'daily_metrics': daily_metrics,
                'audience_insights': audience_insights,
                'creative_performance': creative_performance,
                'recommendations': recommendations
            }
        except FacebookRequestError as e:
            logger.error(f"Facebook API error: {str(e)}")
            return {'error': f"Facebook API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting campaign analytics: {str(e)}")
            return {'error': f"Error getting campaign analytics: {str(e)}"}
    
    def _map_objective(self, objective: str) -> str:
        """
        Map campaign objective
        
        Args:
            objective (str): Campaign objective
            
        Returns:
            str: Facebook campaign objective
        """
        objective_mapping = {
            'awareness': 'BRAND_AWARENESS',
            'consideration': 'TRAFFIC',
            'conversion': 'CONVERSIONS'
        }
        
        return objective_mapping.get(objective, 'BRAND_AWARENESS')
    
    def _map_optimization_goal(self, optimization_goal: str) -> str:
        """
        Map optimization goal
        
        Args:
            optimization_goal (str): Optimization goal
            
        Returns:
            str: Facebook optimization goal
        """
        goal_mapping = {
            'REACH': 'REACH',
            'IMPRESSIONS': 'IMPRESSIONS',
            'LINK_CLICKS': 'LINK_CLICKS',
            'CONVERSIONS': 'CONVERSIONS',
            'PAGE_LIKES': 'PAGE_LIKES',
            'APP_INSTALLS': 'APP_INSTALLS',
            'VIDEO_VIEWS': 'VIDEO_VIEWS'
        }
        
        return goal_mapping.get(optimization_goal, 'IMPRESSIONS')
    
    def _map_call_to_action(self, call_to_action: str) -> str:
        """
        Map call to action
        
        Args:
            call_to_action (str): Call to action
            
        Returns:
            str: Facebook call to action
        """
        cta_mapping = {
            'shop_now': 'SHOP_NOW',
            'book_now': 'BOOK_NOW',
            'learn_more': 'LEARN_MORE',
            'sign_up': 'SIGN_UP',
            'download': 'DOWNLOAD',
            'watch_more': 'WATCH_MORE',
            'contact_us': 'CONTACT_US',
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
            Dict: Facebook targeting object
        """
        fb_targeting = {}
        
        # Age range
        if targeting.age_min:
            fb_targeting['age_min'] = targeting.age_min
        
        if targeting.age_max:
            fb_targeting['age_max'] = targeting.age_max
        
        # Genders
        if targeting.genders:
            gender_mapping = {
                'male': 1,
                'female': 2,
                'all': None
            }
            
            genders = []
            
            for gender in targeting.genders:
                if gender in gender_mapping and gender_mapping[gender]:
                    genders.append(gender_mapping[gender])
            
            if genders:
                fb_targeting['genders'] = genders
        
        # Locations
        if targeting.locations:
            fb_targeting['geo_locations'] = {
                'countries': [],
                'regions': [],
                'cities': []
            }
            
            for location in targeting.locations:
                location_type = location.get('type')
                
                if location_type == 'country':
                    fb_targeting['geo_locations']['countries'].append(location.get('key'))
                elif location_type == 'region':
                    fb_targeting['geo_locations']['regions'].append({
                        'key': location.get('key'),
                        'name': location.get('name'),
                        'country': location.get('country')
                    })
                elif location_type == 'city':
                    fb_targeting['geo_locations']['cities'].append({
                        'key': location.get('key'),
                        'name': location.get('name'),
                        'region': location.get('region'),
                        'country': location.get('country')
                    })
        
        # Interests
        if targeting.interests:
            fb_targeting['flexible_spec'] = [{'interests': []}]
            
            for interest in targeting.interests:
                fb_targeting['flexible_spec'][0]['interests'].append({
                    'id': interest.get('id'),
                    'name': interest.get('name')
                })
        
        # Behaviors
        if targeting.behaviors:
            if 'flexible_spec' not in fb_targeting:
                fb_targeting['flexible_spec'] = [{'behaviors': []}]
            elif 'behaviors' not in fb_targeting['flexible_spec'][0]:
                fb_targeting['flexible_spec'][0]['behaviors'] = []
            
            for behavior in targeting.behaviors:
                fb_targeting['flexible_spec'][0]['behaviors'].append({
                    'id': behavior.get('id'),
                    'name': behavior.get('name')
                })
        
        # Custom audiences
        if targeting.custom_audiences:
            fb_targeting['custom_audiences'] = []
            
            for audience in targeting.custom_audiences:
                fb_targeting['custom_audiences'].append({
                    'id': audience.get('id'),
                    'name': audience.get('name')
                })
        
        # Excluded audiences
        if targeting.excluded_audiences:
            fb_targeting['excluded_custom_audiences'] = []
            
            for audience in targeting.excluded_audiences:
                fb_targeting['excluded_custom_audiences'].append({
                    'id': audience.get('id'),
                    'name': audience.get('name')
                })
        
        # Device platforms
        if targeting.device_platforms:
            fb_targeting['device_platforms'] = targeting.device_platforms
        
        # Platforms
        if targeting.platforms:
            fb_targeting['publisher_platforms'] = targeting.platforms
        
        # Placements
        if targeting.placements:
            fb_targeting['facebook_positions'] = targeting.placements
        
        return fb_targeting
    
    def _upload_image(self, account, image_url: str) -> str:
        """
        Upload image to Facebook
        
        Args:
            account: Ad account
            image_url (str): Image URL
            
        Returns:
            str: Image hash
        """
        # Upload image
        image = account.create_ad_image(
            params={
                'filename': image_url
            }
        )
        
        # Get image hash
        return image['hash']
    
    def _get_audience_insights(self, ad_sets) -> Dict:
        """
        Get audience insights from ad sets
        
        Args:
            ad_sets: Ad sets
            
        Returns:
            Dict: Audience insights
        """
        # Initialize insights
        insights = {
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
        
        # Process ad sets
        for ad_set in ad_sets:
            targeting = ad_set.get('targeting', {})
            
            # Process age and gender
            age_min = targeting.get('age_min', 18)
            age_max = targeting.get('age_max', 65)
            genders = targeting.get('genders', [])
            
            age_ranges = [
                '18-24',
                '25-34',
                '35-44',
                '45-54',
                '55-64',
                '65+'
            ]
            
            gender_mapping = {
                1: 'male',
                2: 'female'
            }
            
            for age_range in age_ranges:
                min_age, max_age = age_range.replace('+', '-100').split('-')
                
                if int(min_age) >= age_min and int(max_age) <= age_max:
                    if not genders:
                        key = f"{age_range} - all"
                        insights['age_gender'][key] = insights['age_gender'].get(key, 0) + 1
                    else:
                        for gender in genders:
                            gender_name = gender_mapping.get(gender, 'unknown')
                            key = f"{age_range} - {gender_name}"
                            insights['age_gender'][key] = insights['age_gender'].get(key, 0) + 1
            
            # Process locations
            geo_locations = targeting.get('geo_locations', {})
            
            for country in geo_locations.get('countries', []):
                insights['locations'][country] = insights['locations'].get(country, 0) + 1
            
            for region in geo_locations.get('regions', []):
                key = f"{region.get('name')}, {region.get('country')}"
                insights['locations'][key] = insights['locations'].get(key, 0) + 1
            
            for city in geo_locations.get('cities', []):
                key = f"{city.get('name')}, {city.get('region')}, {city.get('country')}"
                insights['locations'][key] = insights['locations'].get(key, 0) + 1
            
            # Process interests and behaviors
            flexible_spec = targeting.get('flexible_spec', [])
            
            for spec in flexible_spec:
                for interest in spec.get('interests', []):
                    key = interest.get('name', 'Unknown')
                    insights['interests'][key] = insights['interests'].get(key, 0) + 1
                
                for behavior in spec.get('behaviors', []):
                    key = behavior.get('name', 'Unknown')
                    insights['behaviors'][key] = insights['behaviors'].get(key, 0) + 1
            
            # Process devices and platforms
            device_platforms = targeting.get('device_platforms', [])
            publisher_platforms = targeting.get('publisher_platforms', [])
            facebook_positions = targeting.get('facebook_positions', [])
            
            for device in device_platforms:
                insights['devices'][device] = insights['devices'].get(device, 0) + 1
            
            for platform in publisher_platforms:
                insights['platforms'][platform] = insights['platforms'].get(platform, 0) + 1
            
            for placement in facebook_positions:
                insights['placements'][placement] = insights['placements'].get(placement, 0) + 1
        
        return insights
    
    def _get_creative_performance(self, ads, start_date: str, end_date: str) -> List[Dict]:
        """
        Get creative performance
        
        Args:
            ads: Ads
            start_date (str): Start date
            end_date (str): End date
            
        Returns:
            List[Dict]: Creative performance
        """
        performance = []
        
        for ad in ads:
            try:
                # Get creative
                creative_id = ad.get('creative', {}).get('id')
                
                if not creative_id:
                    continue
                
                # Get insights
                insights = ad.get_insights(
                    fields=[
                        'impressions',
                        'clicks',
                        'spend',
                        'ctr',
                        'cpc',
                        'cpm',
                        'actions',
                        'conversions',
                        'conversion_values'
                    ],
                    params={
                        'time_range': {
                            'since': start_date,
                            'until': end_date
                        }
                    }
                )
                
                if not insights:
                    continue
                
                # Get first insight
                insight = insights[0]
                
                # Get basic metrics
                impressions = int(insight.get('impressions', 0))
                clicks = int(insight.get('clicks', 0))
                spend = float(insight.get('spend', 0))
                
                # Get conversions and revenue
                conversions = 0
                
                if 'actions' in insight:
                    for action in insight['actions']:
                        if action['action_type'] in ['purchase', 'offsite_conversion.fb_pixel_purchase']:
                            conversions += int(action.get('value', 0))
                
                # Calculate metrics
                ctr = float(insight.get('ctr', 0)) * 100
                cpc = float(insight.get('cpc', 0))
                cpm = float(insight.get('cpm', 0))
                conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
                cost_per_conversion = (spend / conversions) if conversions > 0 else 0
                
                # Add to performance
                performance.append({
                    'creative_id': creative_id,
                    'impressions': impressions,
                    'clicks': clicks,
                    'conversions': conversions,
                    'spend': spend,
                    'ctr': ctr,
                    'cpc': cpc,
                    'cpm': cpm,
                    'conversion_rate': conversion_rate,
                    'cost_per_conversion': cost_per_conversion
                })
            except Exception as e:
                logger.error(f"Error getting creative performance: {str(e)}")
                continue
        
        return performance
    
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
        if average_ctr < 1.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'creative',
                'priority': 'high',
                'description': 'Your click-through rate (CTR) is below average. Consider improving your ad creatives with more compelling images and copy.',
                'expected_impact': 'Increasing CTR can lead to more clicks and potentially more conversions.'
            })
        
        # Check CPC
        if average_cpc > 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'targeting',
                'priority': 'medium',
                'description': 'Your cost per click (CPC) is high. Consider refining your targeting to reach a more relevant audience.',
                'expected_impact': 'Reducing CPC can help you get more clicks for your budget.'
            })
        
        # Check conversion rate
        if average_conversion_rate < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'landing_page',
                'priority': 'high',
                'description': 'Your conversion rate is low. Consider improving your landing page experience or ensuring your offer is compelling.',
                'expected_impact': 'Increasing conversion rate directly impacts your return on ad spend.'
            })
        
        # Check creative performance
        if creative_performance:
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
        
        # Check budget allocation
        if total_spend > 0 and total_conversions > 0:
            cost_per_conversion = total_spend / total_conversions
            
            if cost_per_conversion > 50:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'budget',
                    'priority': 'medium',
                    'description': 'Your cost per conversion is high. Consider adjusting your budget or targeting to improve efficiency.',
                    'expected_impact': 'Reducing cost per conversion improves your return on investment.'
                })
        
        return recommendations
