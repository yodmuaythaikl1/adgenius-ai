"""
AdGenius AI Backend - Instagram API Connector
"""
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

try:
    from facebook_business.api import FacebookAdsApi
    from facebook_business.adobjects.adaccount import AdAccount
    from facebook_business.adobjects.campaign import Campaign as FBCampaign
    from facebook_business.adobjects.adset import AdSet
    from facebook_business.adobjects.ad import Ad
    from facebook_business.adobjects.adcreative import AdCreative
    from facebook_business.adobjects.targetingsearch import TargetingSearch
    from facebook_business.adobjects.targeting import Targeting
    from facebook_business.adobjects.iguser import IGUser
    from facebook_business.adobjects.igmedia import IGMedia
    from facebook_business.exceptions import FacebookRequestError
    HAS_FACEBOOK_SDK = True
except ImportError:
    HAS_FACEBOOK_SDK = False
    FacebookRequestError = Exception  # Fallback

from app.models.campaign import Campaign
from app.utils.helpers import generate_id

logger = logging.getLogger(__name__)

class InstagramConnector:
    """Instagram API connector"""
    
    def __init__(self):
        """Initialize Instagram connector"""
        self.app_id = os.getenv('FACEBOOK_APP_ID')  # Instagram uses Facebook API
        self.app_secret = os.getenv('FACEBOOK_APP_SECRET')
        self.api_version = os.getenv('FACEBOOK_API_VERSION', 'v16.0')
        self.initialized = False
    
    def initialize(self, access_token: str):
        """
        Initialize Instagram API (via Facebook Ads API)
        
        Args:
            access_token (str): Access token
        """
        try:
            FacebookAdsApi.init(self.app_id, self.app_secret, access_token, api_version=self.api_version)
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Instagram API: {str(e)}")
            self.initialized = False
    
    def get_instagram_accounts(self, access_token: str) -> List[Dict]:
        """
        Get Instagram business accounts
        
        Args:
            access_token (str): Access token
            
        Returns:
            List[Dict]: Instagram accounts
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Instagram API'}
        
        try:
            # Get Facebook pages
            from facebook_business.adobjects.user import User
            me = User(fbid='me')
            pages = me.get_accounts(fields=['id', 'name', 'instagram_business_account'])
            
            # Filter pages with Instagram business accounts
            result = []
            
            for page in pages:
                if 'instagram_business_account' in page:
                    # Get Instagram account details
                    ig_account_id = page['instagram_business_account']['id']
                    ig_account = IGUser(ig_account_id)
                    ig_account_details = ig_account.api_get(fields=['id', 'username', 'profile_picture_url', 'name', 'biography', 'follows_count', 'followers_count', 'media_count'])
                    
                    result.append({
                        'id': ig_account_id,
                        'username': ig_account_details.get('username'),
                        'name': ig_account_details.get('name'),
                        'profile_picture_url': ig_account_details.get('profile_picture_url'),
                        'biography': ig_account_details.get('biography'),
                        'follows_count': ig_account_details.get('follows_count'),
                        'followers_count': ig_account_details.get('followers_count'),
                        'media_count': ig_account_details.get('media_count'),
                        'facebook_page_id': page['id'],
                        'facebook_page_name': page['name']
                    })
            
            return result
        except FacebookRequestError as e:
            logger.error(f"Instagram API error: {str(e)}")
            return {'error': f"Instagram API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting Instagram accounts: {str(e)}")
            return {'error': f"Error getting Instagram accounts: {str(e)}"}
    
    def search_hashtags(self, access_token: str, query: str) -> List[Dict]:
        """
        Search Instagram hashtags
        
        Args:
            access_token (str): Access token
            query (str): Search query
            
        Returns:
            List[Dict]: Hashtags
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Instagram API'}
        
        try:
            # Get Instagram business account
            from facebook_business.adobjects.user import User
            me = User(fbid='me')
            pages = me.get_accounts(fields=['instagram_business_account'])
            
            if not pages or 'instagram_business_account' not in pages[0]:
                return {'error': 'No Instagram business account found'}
            
            ig_account_id = pages[0]['instagram_business_account']['id']
            ig_account = IGUser(ig_account_id)
            
            # Search hashtags
            hashtags = ig_account.get_instagram_hashtag_search(
                params={
                    'q': query
                }
            )
            
            # Format results
            formatted_results = []
            
            for hashtag in hashtags:
                formatted_results.append({
                    'id': hashtag.get('id'),
                    'name': hashtag.get('name'),
                    'search_result_subtitle': hashtag.get('search_result_subtitle')
                })
            
            return formatted_results
        except FacebookRequestError as e:
            logger.error(f"Instagram API error: {str(e)}")
            return {'error': f"Instagram API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error searching hashtags: {str(e)}")
            return {'error': f"Error searching hashtags: {str(e)}"}
    
    def get_hashtag_insights(self, access_token: str, hashtag_id: str) -> Dict:
        """
        Get hashtag insights
        
        Args:
            access_token (str): Access token
            hashtag_id (str): Hashtag ID
            
        Returns:
            Dict: Hashtag insights
        """
        # Initialize API
        self.initialize(access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Instagram API'}
        
        try:
            # Get Instagram business account
            from facebook_business.adobjects.user import User
            me = User(fbid='me')
            pages = me.get_accounts(fields=['instagram_business_account'])
            
            if not pages or 'instagram_business_account' not in pages[0]:
                return {'error': 'No Instagram business account found'}
            
            ig_account_id = pages[0]['instagram_business_account']['id']
            ig_account = IGUser(ig_account_id)
            
            # Get hashtag
            from facebook_business.adobjects.instagramhashtag import InstagramHashtag
            hashtag = InstagramHashtag(hashtag_id)
            
            # Get insights
            insights = hashtag.api_get(
                fields=[
                    'id',
                    'name',
                    'media_count'
                ]
            )
            
            # Get recent media
            recent_media = hashtag.get_recent_media(
                fields=[
                    'id',
                    'caption',
                    'comments_count',
                    'like_count',
                    'media_type',
                    'media_url',
                    'permalink',
                    'timestamp'
                ],
                params={
                    'limit': 10
                }
            )
            
            # Format media
            formatted_media = []
            
            for media in recent_media:
                formatted_media.append({
                    'id': media.get('id'),
                    'caption': media.get('caption'),
                    'comments_count': media.get('comments_count'),
                    'like_count': media.get('like_count'),
                    'media_type': media.get('media_type'),
                    'media_url': media.get('media_url'),
                    'permalink': media.get('permalink'),
                    'timestamp': media.get('timestamp')
                })
            
            return {
                'id': insights.get('id'),
                'name': insights.get('name'),
                'media_count': insights.get('media_count'),
                'recent_media': formatted_media
            }
        except FacebookRequestError as e:
            logger.error(f"Instagram API error: {str(e)}")
            return {'error': f"Instagram API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting hashtag insights: {str(e)}")
            return {'error': f"Error getting hashtag insights: {str(e)}"}
    
    def publish_campaign(self, campaign: Campaign) -> Dict:
        """
        Publish campaign to Instagram
        
        Args:
            campaign (Campaign): Campaign
            
        Returns:
            Dict: Result with platform ID
        """
        # Get user
        user = campaign.user
        
        # Find Instagram account
        instagram_account = None
        
        for account in user.platform_accounts:
            if account.platform == 'instagram':
                instagram_account = account
                break
        
        if not instagram_account:
            return {'error': 'No Instagram account found'}
        
        # Initialize API
        self.initialize(instagram_account.access_token)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Instagram API'}
        
        try:
            # Get ad account
            account = AdAccount(instagram_account.meta_data.get('ad_account_id'))
            
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
            
            # Add Instagram-specific targeting
            targeting['publisher_platforms'] = ['instagram']
            targeting['instagram_positions'] = ['stream', 'story', 'explore']
            
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
                            'instagram_actor_id': instagram_account.account_id,
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
            logger.error(f"Instagram API error: {str(e)}")
            return {'error': f"Instagram API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error publishing campaign: {str(e)}")
            return {'error': f"Error publishing campaign: {str(e)}"}
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """
        Pause Instagram campaign
        
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
            logger.error(f"Instagram API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error pausing campaign: {str(e)}")
            return False
    
    def resume_campaign(self, campaign_id: str) -> bool:
        """
        Resume Instagram campaign
        
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
            logger.error(f"Instagram API error: {str(e)}")
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
            logger.error(f"Instagram API error: {str(e)}")
            return {'error': f"Instagram API error: {e.api_error_message()}"}
        except Exception as e:
            logger.error(f"Error getting campaign analytics: {str(e)}")
            return {'error': f"Error getting campaign analytics: {str(e)}"}
    
    def _map_objective(self, objective: str) -> str:
        """
        Map campaign objective
        
        Args:
            objective (str): Campaign objective
            
        Returns:
            str: Instagram campaign objective
        """
        objective_mapping = {
            'awareness': 'BRAND_AWARENESS',
            'consideration': 'REACH',
            'conversion': 'CONVERSIONS'
        }
        
        return objective_mapping.get(objective, 'REACH')
    
    def _map_optimization_goal(self, optimization_goal: str) -> str:
        """
        Map optimization goal
        
        Args:
            optimization_goal (str): Optimization goal
            
        Returns:
            str: Instagram optimization goal
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
        
        return goal_mapping.get(optimization_goal, 'REACH')
    
    def _map_call_to_action(self, call_to_action: str) -> str:
        """
        Map call to action
        
        Args:
            call_to_action (str): Call to action
            
        Returns:
            str: Instagram call to action
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
            Dict: Instagram targeting object
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
        
        return fb_targeting
    
    def _upload_image(self, account, image_url: str) -> str:
        """
        Upload image to Instagram
        
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
            instagram_positions = targeting.get('instagram_positions', [])
            
            for device in device_platforms:
                insights['devices'][device] = insights['devices'].get(device, 0) + 1
            
            for platform in publisher_platforms:
                insights['platforms'][platform] = insights['platforms'].get(platform, 0) + 1
            
            for placement in instagram_positions:
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
        if average_ctr < 0.8:  # Instagram typically has lower CTR than Facebook
            recommendations.append({
                'id': generate_id(),
                'type': 'creative',
                'priority': 'high',
                'description': 'Your click-through rate (CTR) is below average for Instagram. Consider using more visually appealing images or videos with clear call-to-actions.',
                'expected_impact': 'Increasing CTR can lead to more clicks and potentially more conversions.'
            })
        
        # Check CPC
        if average_cpc > 2.5:  # Instagram typically has higher CPC than Facebook
            recommendations.append({
                'id': generate_id(),
                'type': 'targeting',
                'priority': 'medium',
                'description': 'Your cost per click (CPC) is high for Instagram. Consider refining your targeting to reach a more relevant audience.',
                'expected_impact': 'Reducing CPC can help you get more clicks for your budget.'
            })
        
        # Check conversion rate
        if average_conversion_rate < 1.5:  # Instagram typically has lower conversion rates
            recommendations.append({
                'id': generate_id(),
                'type': 'landing_page',
                'priority': 'high',
                'description': 'Your conversion rate is low. Consider improving your landing page experience or ensuring your offer is compelling.',
                'expected_impact': 'Increasing conversion rate directly impacts your return on ad spend.'
            })
        
        # Instagram-specific recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'creative',
            'priority': 'medium',
            'description': 'Consider using Instagram Stories format for your ads. Stories have higher engagement rates and can be more cost-effective.',
            'expected_impact': 'Stories ads can increase engagement and reduce costs.'
        })
        
        recommendations.append({
            'id': generate_id(),
            'type': 'targeting',
            'priority': 'low',
            'description': 'Use hashtag targeting to reach users interested in specific topics related to your product.',
            'expected_impact': 'Hashtag targeting can help reach more relevant audiences.'
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
        
        return recommendations
