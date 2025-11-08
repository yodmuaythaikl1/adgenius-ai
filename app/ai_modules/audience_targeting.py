"""
AdGenius AI Backend - Audience Targeting AI Module
"""
import os
import json
import logging
import time
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta

# Lazy imports - only import when needed
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
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

from app.utils.helpers import generate_id
from app.platform_connectors.facebook_connector import FacebookConnector
from app.platform_connectors.instagram_connector import InstagramConnector
from app.platform_connectors.tiktok_connector import TikTokConnector
from app.platform_connectors.shopee_connector import ShopeeConnector

logger = logging.getLogger(__name__)

class AudienceTargetingAI:
    """Audience Targeting AI Module"""
    
    def __init__(self):
        """Initialize Audience Targeting AI"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.facebook_connector = FacebookConnector()
        self.instagram_connector = InstagramConnector()
        self.tiktok_connector = TikTokConnector()
        self.shopee_connector = ShopeeConnector()
        
        # Initialize OpenAI client if available
        if HAS_OPENAI and self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def analyze_product(self, product_description: str, product_category: str, target_audience: str = None) -> Dict:
        """
        Analyze product to identify key features and target audience
        
        Args:
            product_description (str): Product description
            product_category (str): Product category
            target_audience (str, optional): Target audience description
            
        Returns:
            Dict: Product analysis
        """
        try:
            # Prepare prompt
            prompt = f"""
            Analyze the following product and identify key features, benefits, and target audience:
            
            Product Category: {product_category}
            Product Description: {product_description}
            """
            
            if target_audience:
                prompt += f"\nTarget Audience: {target_audience}"
            
            prompt += """
            
            Please provide the following information:
            1. Key product features
            2. Main benefits
            3. Target audience demographics (age range, gender, income level)
            4. Target audience interests
            5. Target audience behaviors
            6. Keywords for targeting
            7. Recommended platforms for advertising
            
            Format your response as JSON with the following structure:
            {
                "features": ["feature1", "feature2", ...],
                "benefits": ["benefit1", "benefit2", ...],
                "target_audience": {
                    "age_range": {"min": 18, "max": 65},
                    "genders": ["female", "male"],
                    "income_levels": ["middle", "high"]
                },
                "interests": ["interest1", "interest2", ...],
                "behaviors": ["behavior1", "behavior2", ...],
                "keywords": ["keyword1", "keyword2", ...],
                "recommended_platforms": ["facebook", "instagram", "tiktok", "shopee"]
            }
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in audience targeting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse response
            content = response.choices[0].message.content
            
            # Extract JSON
            start_index = content.find('{')
            end_index = content.rfind('}') + 1
            
            if start_index == -1 or end_index == 0:
                return {'error': 'Failed to parse AI response'}
            
            json_content = content[start_index:end_index]
            
            # Parse JSON
            result = json.loads(json_content)
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing product: {str(e)}")
            return {'error': f"Error analyzing product: {str(e)}"}
    
    def generate_targeting_strategy(self, product_analysis: Dict, platform: str) -> Dict:
        """
        Generate targeting strategy for a specific platform
        
        Args:
            product_analysis (Dict): Product analysis
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            
        Returns:
            Dict: Targeting strategy
        """
        try:
            # Extract targeting information
            target_audience = product_analysis.get('target_audience', {})
            interests = product_analysis.get('interests', [])
            behaviors = product_analysis.get('behaviors', [])
            keywords = product_analysis.get('keywords', [])
            
            # Prepare platform-specific targeting
            if platform == 'facebook':
                return self._generate_facebook_targeting(target_audience, interests, behaviors, keywords)
            elif platform == 'instagram':
                return self._generate_instagram_targeting(target_audience, interests, behaviors, keywords)
            elif platform == 'tiktok':
                return self._generate_tiktok_targeting(target_audience, interests, behaviors, keywords)
            elif platform == 'shopee':
                return self._generate_shopee_targeting(target_audience, interests, behaviors, keywords)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error generating targeting strategy: {str(e)}")
            return {'error': f"Error generating targeting strategy: {str(e)}"}
    
    def find_target_keywords(self, product_description: str, platform: str, access_token: str, account_id: str = None) -> List[Dict]:
        """
        Find target keywords for a specific platform
        
        Args:
            product_description (str): Product description
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            access_token (str): Access token
            account_id (str, optional): Account ID
            
        Returns:
            List[Dict]: Target keywords
        """
        try:
            # Extract keywords from product description
            keywords = self._extract_keywords(product_description)
            
            # Find platform-specific keywords
            if platform == 'facebook':
                self.facebook_connector.initialize(access_token)
                return self._find_facebook_keywords(keywords, access_token)
            elif platform == 'instagram':
                self.instagram_connector.initialize(access_token)
                return self._find_instagram_keywords(keywords, access_token)
            elif platform == 'tiktok':
                self.tiktok_connector.initialize(access_token)
                return self._find_tiktok_keywords(keywords, account_id)
            elif platform == 'shopee':
                self.shopee_connector.initialize(access_token, account_id)
                return self._find_shopee_keywords(keywords)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error finding target keywords: {str(e)}")
            return {'error': f"Error finding target keywords: {str(e)}"}
    
    def analyze_audience_performance(self, platform: str, campaign_id: str, access_token: str, account_id: str = None, start_date: datetime = None, end_date: datetime = None) -> Dict:
        """
        Analyze audience performance for a specific campaign
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            start_date (datetime, optional): Start date
            end_date (datetime, optional): End date
            
        Returns:
            Dict: Audience performance analysis
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
                return self._analyze_facebook_audience(campaign_id, start_date, end_date)
            elif platform == 'instagram':
                self.instagram_connector.initialize(access_token)
                return self._analyze_instagram_audience(campaign_id, start_date, end_date)
            elif platform == 'tiktok':
                self.tiktok_connector.initialize(access_token)
                return self._analyze_tiktok_audience(account_id, campaign_id, start_date, end_date)
            elif platform == 'shopee':
                self.shopee_connector.initialize(access_token, account_id)
                return self._analyze_shopee_audience(start_date, end_date)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error analyzing audience performance: {str(e)}")
            return {'error': f"Error analyzing audience performance: {str(e)}"}
    
    def optimize_audience_targeting(self, platform: str, campaign_id: str, access_token: str, account_id: str = None) -> Dict:
        """
        Optimize audience targeting for a specific campaign
        
        Args:
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            campaign_id (str): Campaign ID
            access_token (str): Access token
            account_id (str, optional): Account ID
            
        Returns:
            Dict: Optimized audience targeting
        """
        try:
            # Get audience performance
            performance = self.analyze_audience_performance(
                platform=platform,
                campaign_id=campaign_id,
                access_token=access_token,
                account_id=account_id
            )
            
            if 'error' in performance:
                return performance
            
            # Generate optimized targeting
            if platform == 'facebook':
                return self._optimize_facebook_targeting(performance)
            elif platform == 'instagram':
                return self._optimize_instagram_targeting(performance)
            elif platform == 'tiktok':
                return self._optimize_tiktok_targeting(performance)
            elif platform == 'shopee':
                return self._optimize_shopee_targeting(performance)
            else:
                return {'error': f"Unsupported platform: {platform}"}
        except Exception as e:
            logger.error(f"Error optimizing audience targeting: {str(e)}")
            return {'error': f"Error optimizing audience targeting: {str(e)}"}
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text (str): Text
            
        Returns:
            List[str]: Keywords
        """
        # Prepare prompt
        prompt = f"""
        Extract the most important keywords from the following text that would be useful for targeting advertisements:
        
        {text}
        
        Please provide a list of keywords in JSON format:
        ["keyword1", "keyword2", "keyword3", ...]
        
        Focus on keywords that would be useful for targeting advertisements, such as product features, benefits, use cases, and target audience characteristics.
        """
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI marketing expert specializing in keyword extraction."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        # Parse response
        content = response.choices[0].message.content
        
        # Extract JSON
        start_index = content.find('[')
        end_index = content.rfind(']') + 1
        
        if start_index == -1 or end_index == 0:
            return []
        
        json_content = content[start_index:end_index]
        
        # Parse JSON
        try:
            keywords = json.loads(json_content)
            return keywords
        except:
            # Fallback to simple extraction
            words = text.lower().split()
            return list(set([word for word in words if len(word) > 3]))
    
    def _generate_facebook_targeting(self, target_audience: Dict, interests: List[str], behaviors: List[str], keywords: List[str]) -> Dict:
        """
        Generate Facebook targeting
        
        Args:
            target_audience (Dict): Target audience
            interests (List[str]): Interests
            behaviors (List[str]): Behaviors
            keywords (List[str]): Keywords
            
        Returns:
            Dict: Facebook targeting
        """
        # Map age range
        age_range = target_audience.get('age_range', {})
        age_min = age_range.get('min', 18)
        age_max = age_range.get('max', 65)
        
        # Map genders
        genders = target_audience.get('genders', ['female', 'male'])
        
        # Prepare targeting
        targeting = {
            'age_min': age_min,
            'age_max': age_max,
            'genders': genders,
            'interests': [{'name': interest} for interest in interests],
            'behaviors': [{'name': behavior} for behavior in behaviors],
            'keywords': keywords,
            'optimization_goal': 'CONVERSIONS',
            'recommended_bid_strategy': 'LOWEST_COST_WITH_BID_CAP'
        }
        
        return targeting
    
    def _generate_instagram_targeting(self, target_audience: Dict, interests: List[str], behaviors: List[str], keywords: List[str]) -> Dict:
        """
        Generate Instagram targeting
        
        Args:
            target_audience (Dict): Target audience
            interests (List[str]): Interests
            behaviors (List[str]): Behaviors
            keywords (List[str]): Keywords
            
        Returns:
            Dict: Instagram targeting
        """
        # Instagram uses Facebook targeting with some modifications
        facebook_targeting = self._generate_facebook_targeting(target_audience, interests, behaviors, keywords)
        
        # Add Instagram-specific targeting
        facebook_targeting['placements'] = ['instagram_feed', 'instagram_stories', 'instagram_explore']
        facebook_targeting['optimization_goal'] = 'REACH'
        
        # Add hashtags
        facebook_targeting['hashtags'] = [f"#{keyword.replace(' ', '')}" for keyword in keywords]
        
        return facebook_targeting
    
    def _generate_tiktok_targeting(self, target_audience: Dict, interests: List[str], behaviors: List[str], keywords: List[str]) -> Dict:
        """
        Generate TikTok targeting
        
        Args:
            target_audience (Dict): Target audience
            interests (List[str]): Interests
            behaviors (List[str]): Behaviors
            keywords (List[str]): Keywords
            
        Returns:
            Dict: TikTok targeting
        """
        # Map age range
        age_range = target_audience.get('age_range', {})
        age_min = age_range.get('min', 18)
        age_max = age_range.get('max', 65)
        
        # Map age groups
        age_groups = []
        
        if age_min <= 17 and age_max >= 13:
            age_groups.append('AGE_13_17')
        
        if age_min <= 24 and age_max >= 18:
            age_groups.append('AGE_18_24')
        
        if age_min <= 34 and age_max >= 25:
            age_groups.append('AGE_25_34')
        
        if age_min <= 44 and age_max >= 35:
            age_groups.append('AGE_35_44')
        
        if age_min <= 54 and age_max >= 45:
            age_groups.append('AGE_45_54')
        
        if age_max >= 55:
            age_groups.append('AGE_55_100')
        
        # Map genders
        genders = []
        
        for gender in target_audience.get('genders', ['female', 'male']):
            if gender == 'female':
                genders.append('GENDER_FEMALE')
            elif gender == 'male':
                genders.append('GENDER_MALE')
        
        # Prepare targeting
        targeting = {
            'age': age_groups,
            'gender': genders,
            'interest_category_ids': [],
            'behavior_ids': [],
            'hashtags': [keyword.replace(' ', '') for keyword in keywords],
            'optimization_goal': 'CONVERSION',
            'recommended_bid_strategy': 'BID_TYPE_CUSTOM'
        }
        
        return targeting
    
    def _generate_shopee_targeting(self, target_audience: Dict, interests: List[str], behaviors: List[str], keywords: List[str]) -> Dict:
        """
        Generate Shopee targeting
        
        Args:
            target_audience (Dict): Target audience
            interests (List[str]): Interests
            behaviors (List[str]): Behaviors
            keywords (List[str]): Keywords
            
        Returns:
            Dict: Shopee targeting
        """
        # Shopee doesn't have traditional targeting like social platforms
        # Instead, we focus on product optimization and keywords
        
        # Prepare targeting
        targeting = {
            'keywords': keywords,
            'product_optimization': {
                'title_keywords': keywords[:5],  # Top 5 keywords for title
                'description_keywords': keywords,  # All keywords for description
                'recommended_price_range': {
                    'min': 0,
                    'max': 0
                },
                'recommended_discount': 10  # 10% discount
            },
            'promotion_strategy': {
                'recommended_promotion_type': 'daily_discover',
                'recommended_boost_frequency': 'daily'
            }
        }
        
        return targeting
    
    def _find_facebook_keywords(self, keywords: List[str], access_token: str) -> List[Dict]:
        """
        Find Facebook keywords
        
        Args:
            keywords (List[str]): Keywords
            access_token (str): Access token
            
        Returns:
            List[Dict]: Facebook keywords
        """
        results = []
        
        for keyword in keywords:
            # Search for interests
            interests = self.facebook_connector.search_targeting_keywords(access_token, keyword, 'interests')
            
            if isinstance(interests, list):
                for interest in interests:
                    results.append({
                        'id': interest.get('id'),
                        'name': interest.get('name'),
                        'type': 'interest',
                        'audience_size': interest.get('audience_size'),
                        'source_keyword': keyword
                    })
            
            # Search for behaviors
            behaviors = self.facebook_connector.search_targeting_keywords(access_token, keyword, 'behaviors')
            
            if isinstance(behaviors, list):
                for behavior in behaviors:
                    results.append({
                        'id': behavior.get('id'),
                        'name': behavior.get('name'),
                        'type': 'behavior',
                        'audience_size': behavior.get('audience_size'),
                        'source_keyword': keyword
                    })
        
        # Sort by audience size
        results.sort(key=lambda x: x.get('audience_size', 0), reverse=True)
        
        return results
    
    def _find_instagram_keywords(self, keywords: List[str], access_token: str) -> List[Dict]:
        """
        Find Instagram keywords
        
        Args:
            keywords (List[str]): Keywords
            access_token (str): Access token
            
        Returns:
            List[Dict]: Instagram keywords
        """
        results = []
        
        for keyword in keywords:
            # Search for hashtags
            hashtags = self.instagram_connector.search_hashtags(access_token, keyword)
            
            if isinstance(hashtags, list):
                for hashtag in hashtags:
                    results.append({
                        'id': hashtag.get('id'),
                        'name': hashtag.get('name'),
                        'type': 'hashtag',
                        'source_keyword': keyword
                    })
        
        # Add Facebook interests and behaviors
        facebook_keywords = self._find_facebook_keywords(keywords, access_token)
        
        if isinstance(facebook_keywords, list):
            results.extend(facebook_keywords)
        
        return results
    
    def _find_tiktok_keywords(self, keywords: List[str], advertiser_id: str) -> List[Dict]:
        """
        Find TikTok keywords
        
        Args:
            keywords (List[str]): Keywords
            advertiser_id (str): Advertiser ID
            
        Returns:
            List[Dict]: TikTok keywords
        """
        results = []
        
        for keyword in keywords:
            # Search for interests
            interests = self.tiktok_connector.search_targeting_keywords(advertiser_id, keyword, 'interest_category')
            
            if isinstance(interests, list):
                for interest in interests:
                    results.append({
                        'id': interest.get('id'),
                        'name': interest.get('name'),
                        'type': 'interest',
                        'audience_size': interest.get('audience_size'),
                        'source_keyword': keyword
                    })
            
            # Search for hashtags
            hashtags = self.tiktok_connector.search_hashtags(advertiser_id, keyword)
            
            if isinstance(hashtags, list):
                for hashtag in hashtags:
                    results.append({
                        'id': hashtag.get('id'),
                        'name': hashtag.get('name'),
                        'type': 'hashtag',
                        'audience_size': hashtag.get('audience_size'),
                        'source_keyword': keyword
                    })
        
        # Sort by audience size
        results.sort(key=lambda x: x.get('audience_size', 0), reverse=True)
        
        return results
    
    def _find_shopee_keywords(self, keywords: List[str]) -> List[Dict]:
        """
        Find Shopee keywords
        
        Args:
            keywords (List[str]): Keywords
            
        Returns:
            List[Dict]: Shopee keywords
        """
        # Shopee doesn't have a direct keyword search API
        # Instead, we'll return the keywords with estimated search volume
        
        results = []
        
        for keyword in keywords:
            # Simulate search volume (in a real implementation, this would come from Shopee API)
            search_volume = np.random.randint(100, 10000)
            
            results.append({
                'keyword': keyword,
                'search_volume': search_volume,
                'type': 'product_keyword'
            })
        
        # Sort by search volume
        results.sort(key=lambda x: x.get('search_volume', 0), reverse=True)
        
        return results
    
    def _analyze_facebook_audience(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Facebook audience
        
        Args:
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Audience analysis
        """
        # Get campaign analytics
        analytics = self.facebook_connector.get_campaign_analytics(campaign_id, start_date, end_date)
        
        if 'error' in analytics:
            return analytics
        
        # Extract audience insights
        audience_insights = analytics.get('audience_insights', {})
        
        # Process age and gender
        age_gender = {}
        
        for key, value in audience_insights.get('age_gender', {}).items():
            age_gender[key] = value
        
        # Process locations
        locations = {}
        
        for key, value in audience_insights.get('locations', {}).items():
            locations[key] = value
        
        # Process interests
        interests = {}
        
        for key, value in audience_insights.get('interests', {}).items():
            interests[key] = value
        
        # Process behaviors
        behaviors = {}
        
        for key, value in audience_insights.get('behaviors', {}).items():
            behaviors[key] = value
        
        # Calculate performance metrics
        total_impressions = analytics.get('total_impressions', 0)
        total_clicks = analytics.get('total_clicks', 0)
        total_conversions = analytics.get('total_conversions', 0)
        
        # Calculate CTR by audience segment
        ctr_by_age_gender = {}
        
        for key, value in age_gender.items():
            if isinstance(value, dict):
                impressions = value.get('impressions', 0)
                clicks = value.get('clicks', 0)
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                ctr_by_age_gender[key] = ctr
        
        # Find best performing segments
        best_age_gender = max(ctr_by_age_gender.items(), key=lambda x: x[1]) if ctr_by_age_gender else ('unknown', 0)
        best_interests = sorted(interests.items(), key=lambda x: x[1], reverse=True)[:5] if interests else []
        best_behaviors = sorted(behaviors.items(), key=lambda x: x[1], reverse=True)[:5] if behaviors else []
        
        return {
            'audience_insights': {
                'age_gender': age_gender,
                'locations': locations,
                'interests': interests,
                'behaviors': behaviors
            },
            'performance_metrics': {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions,
                'ctr_by_age_gender': ctr_by_age_gender
            },
            'best_performing_segments': {
                'age_gender': best_age_gender,
                'interests': best_interests,
                'behaviors': best_behaviors
            }
        }
    
    def _analyze_instagram_audience(self, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Instagram audience
        
        Args:
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Audience analysis
        """
        # Instagram uses Facebook's analytics
        return self._analyze_facebook_audience(campaign_id, start_date, end_date)
    
    def _analyze_tiktok_audience(self, advertiser_id: str, campaign_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze TikTok audience
        
        Args:
            advertiser_id (str): Advertiser ID
            campaign_id (str): Campaign ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Audience analysis
        """
        # Get campaign analytics
        analytics = self.tiktok_connector.get_campaign_analytics(advertiser_id, campaign_id, start_date, end_date)
        
        if 'error' in analytics:
            return analytics
        
        # Extract audience insights
        audience_insights = analytics.get('audience_insights', {})
        
        # Process age and gender
        age_gender = {}
        
        for key, value in audience_insights.get('age_gender', {}).items():
            age_gender[key] = value
        
        # Calculate performance metrics
        total_impressions = analytics.get('total_impressions', 0)
        total_clicks = analytics.get('total_clicks', 0)
        total_conversions = analytics.get('total_conversions', 0)
        
        # Calculate video metrics
        video_metrics = analytics.get('video_metrics', {})
        
        return {
            'audience_insights': {
                'age_gender': age_gender
            },
            'performance_metrics': {
                'total_impressions': total_impressions,
                'total_clicks': total_clicks,
                'total_conversions': total_conversions
            },
            'video_metrics': video_metrics
        }
    
    def _analyze_shopee_audience(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Analyze Shopee audience
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Audience analysis
        """
        # Get shop performance
        performance = self.shopee_connector.get_shop_performance(start_date, end_date)
        
        if 'error' in performance:
            return performance
        
        # Calculate metrics
        total_views = performance.get('total_views', 0)
        total_orders = performance.get('total_orders', 0)
        total_revenue = performance.get('total_revenue', 0)
        conversion_rate = performance.get('conversion_rate', 0)
        
        return {
            'performance_metrics': {
                'total_views': total_views,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'conversion_rate': conversion_rate
            }
        }
    
    def _optimize_facebook_targeting(self, performance: Dict) -> Dict:
        """
        Optimize Facebook targeting
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized targeting
        """
        # Extract best performing segments
        best_segments = performance.get('best_performing_segments', {})
        best_age_gender = best_segments.get('age_gender', ('unknown', 0))
        best_interests = best_segments.get('interests', [])
        best_behaviors = best_segments.get('behaviors', [])
        
        # Parse age and gender
        age_gender_parts = best_age_gender[0].split(' - ')
        
        age_range = age_gender_parts[0] if len(age_gender_parts) > 0 else '18-65'
        gender = age_gender_parts[1] if len(age_gender_parts) > 1 else 'all'
        
        age_min, age_max = age_range.replace('+', '-100').split('-')
        
        # Prepare optimized targeting
        targeting = {
            'age_min': int(age_min),
            'age_max': int(age_max),
            'genders': [gender] if gender != 'all' else ['female', 'male'],
            'interests': [{'name': interest[0]} for interest in best_interests],
            'behaviors': [{'name': behavior[0]} for behavior in best_behaviors],
            'optimization_goal': 'CONVERSIONS',
            'recommended_bid_strategy': 'LOWEST_COST_WITH_BID_CAP'
        }
        
        return targeting
    
    def _optimize_instagram_targeting(self, performance: Dict) -> Dict:
        """
        Optimize Instagram targeting
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized targeting
        """
        # Instagram uses Facebook's targeting with some modifications
        facebook_targeting = self._optimize_facebook_targeting(performance)
        
        # Add Instagram-specific targeting
        facebook_targeting['placements'] = ['instagram_feed', 'instagram_stories', 'instagram_explore']
        facebook_targeting['optimization_goal'] = 'REACH'
        
        return facebook_targeting
    
    def _optimize_tiktok_targeting(self, performance: Dict) -> Dict:
        """
        Optimize TikTok targeting
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized targeting
        """
        # TikTok doesn't provide detailed audience insights yet
        # Return a generic targeting strategy
        
        return {
            'age': ['AGE_18_24', 'AGE_25_34'],
            'gender': ['GENDER_FEMALE', 'GENDER_MALE'],
            'interest_category_ids': [],
            'behavior_ids': [],
            'optimization_goal': 'CONVERSION',
            'recommended_bid_strategy': 'BID_TYPE_CUSTOM'
        }
    
    def _optimize_shopee_targeting(self, performance: Dict) -> Dict:
        """
        Optimize Shopee targeting
        
        Args:
            performance (Dict): Performance data
            
        Returns:
            Dict: Optimized targeting
        """
        # Shopee doesn't have traditional targeting
        # Return product optimization recommendations
        
        return {
            'product_optimization': {
                'recommended_price_range': {
                    'min': 0,
                    'max': 0
                },
                'recommended_discount': 10  # 10% discount
            },
            'promotion_strategy': {
                'recommended_promotion_type': 'daily_discover',
                'recommended_boost_frequency': 'daily'
            }
        }
