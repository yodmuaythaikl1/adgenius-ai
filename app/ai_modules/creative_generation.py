"""
AdGenius AI Backend - Creative Generation AI Module
"""
import os
import json
import logging
import time
import base64
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from app.utils.helpers import generate_id

logger = logging.getLogger(__name__)

class CreativeGenerationAI:
    """Creative Generation AI Module"""
    
    def __init__(self):
        """Initialize Creative Generation AI"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize OpenAI client if available
        if HAS_OPENAI and self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def generate_ad_copy(self, product_name: str, product_description: str, target_audience: str, platform: str, tone: str = 'professional', length: str = 'medium') -> Dict:
        """
        Generate ad copy for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            tone (str, optional): Tone of the ad copy. Defaults to 'professional'.
            length (str, optional): Length of the ad copy. Defaults to 'medium'.
            
        Returns:
            Dict: Generated ad copy
        """
        try:
            # Map length to token count
            length_map = {
                'short': 50,
                'medium': 100,
                'long': 200
            }
            
            max_tokens = length_map.get(length, 100)
            
            # Prepare prompt
            prompt = f"""
            Generate ad copy for the following product:
            
            Product Name: {product_name}
            Product Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Tone: {tone}
            
            The ad copy should be compelling, highlight key benefits, and include a call to action.
            
            For Facebook/Instagram, include a headline, main text, and call to action.
            For TikTok, include a catchy hook and script for a short video.
            For Shopee, include a product title and description optimized for search.
            
            Format your response as JSON with the following structure:
            {{
                "headline": "Compelling headline",
                "main_text": "Main ad copy text",
                "call_to_action": "Call to action text",
                "keywords": ["keyword1", "keyword2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in ad copy generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=max_tokens * 2  # Double the tokens to account for JSON structure
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
            
            # Add metadata
            result['platform'] = platform
            result['tone'] = tone
            result['length'] = length
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating ad copy: {str(e)}")
            return {'error': f"Error generating ad copy: {str(e)}"}
    
    def generate_ad_image(self, product_name: str, product_description: str, target_audience: str, platform: str, style: str = 'professional', size: str = 'square') -> Dict:
        """
        Generate ad image for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            style (str, optional): Style of the image. Defaults to 'professional'.
            size (str, optional): Size of the image. Defaults to 'square'.
            
        Returns:
            Dict: Generated ad image
        """
        try:
            # Map size to dimensions
            size_map = {
                'square': '1024x1024',
                'portrait': '1024x1280',
                'landscape': '1280x1024',
                'facebook': '1200x628',
                'instagram': '1080x1080',
                'tiktok': '1080x1920',
                'shopee': '1000x1000'
            }
            
            # Use platform-specific size if available, otherwise use the specified size
            image_size = size_map.get(platform, size_map.get(size, '1024x1024'))
            
            # Prepare prompt
            prompt = f"""
            Create an advertisement image for:
            
            Product: {product_name}
            Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Style: {style}
            
            The image should be visually appealing, highlight the product, and resonate with the target audience.
            """
            
            # Call OpenAI API
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size=image_size
            )
            
            # Get image URL
            image_url = response['data'][0]['url']
            
            # Download image
            image_response = requests.get(image_url)
            image_data = image_response.content
            
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare result
            result = {
                'image_url': image_url,
                'image_base64': image_base64,
                'platform': platform,
                'style': style,
                'size': size,
                'dimensions': image_size,
                'id': generate_id(),
                'created_at': datetime.now().isoformat()
            }
            
            return result
        except Exception as e:
            logger.error(f"Error generating ad image: {str(e)}")
            return {'error': f"Error generating ad image: {str(e)}"}
    
    def generate_ad_variations(self, ad_copy: Dict, variations_count: int = 3) -> List[Dict]:
        """
        Generate variations of ad copy
        
        Args:
            ad_copy (Dict): Original ad copy
            variations_count (int, optional): Number of variations to generate. Defaults to 3.
            
        Returns:
            List[Dict]: Generated ad copy variations
        """
        try:
            # Extract original ad copy
            headline = ad_copy.get('headline', '')
            main_text = ad_copy.get('main_text', '')
            call_to_action = ad_copy.get('call_to_action', '')
            platform = ad_copy.get('platform', 'facebook')
            tone = ad_copy.get('tone', 'professional')
            
            # Prepare prompt
            prompt = f"""
            Generate {variations_count} variations of the following ad copy:
            
            Headline: {headline}
            Main Text: {main_text}
            Call to Action: {call_to_action}
            Platform: {platform}
            Tone: {tone}
            
            Each variation should maintain the same message but use different wording, structure, or emphasis.
            
            Format your response as JSON with the following structure:
            {{
                "variations": [
                    {{
                        "headline": "Variation 1 headline",
                        "main_text": "Variation 1 main text",
                        "call_to_action": "Variation 1 call to action"
                    }},
                    ...
                ]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in ad copy generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
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
            
            # Add metadata to each variation
            variations = result.get('variations', [])
            
            for i, variation in enumerate(variations):
                variation['platform'] = platform
                variation['tone'] = tone
                variation['id'] = f"{ad_copy.get('id', generate_id())}_var_{i+1}"
                variation['created_at'] = datetime.now().isoformat()
            
            return variations
        except Exception as e:
            logger.error(f"Error generating ad variations: {str(e)}")
            return {'error': f"Error generating ad variations: {str(e)}"}
    
    def generate_social_media_post(self, product_name: str, product_description: str, target_audience: str, platform: str, tone: str = 'professional', include_hashtags: bool = True) -> Dict:
        """
        Generate social media post for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str): Platform (facebook, instagram, tiktok)
            tone (str, optional): Tone of the post. Defaults to 'professional'.
            include_hashtags (bool, optional): Whether to include hashtags. Defaults to True.
            
        Returns:
            Dict: Generated social media post
        """
        try:
            # Prepare prompt
            prompt = f"""
            Generate a social media post for the following product:
            
            Product Name: {product_name}
            Product Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Tone: {tone}
            Include Hashtags: {'Yes' if include_hashtags else 'No'}
            
            The post should be engaging, highlight key benefits, and encourage engagement.
            
            For Facebook, create a longer, more detailed post.
            For Instagram, create a visually descriptive post with relevant hashtags.
            For TikTok, create a short, catchy post that could accompany a video.
            
            Format your response as JSON with the following structure:
            {{
                "caption": "Main post text",
                "hashtags": ["hashtag1", "hashtag2", ...],
                "emojis": ["emoji1", "emoji2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in social media content creation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
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
            
            # Add metadata
            result['platform'] = platform
            result['tone'] = tone
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating social media post: {str(e)}")
            return {'error': f"Error generating social media post: {str(e)}"}
    
    def generate_product_description(self, product_name: str, product_features: List[str], target_audience: str, platform: str = 'shopee', length: str = 'medium') -> Dict:
        """
        Generate product description for e-commerce platforms
        
        Args:
            product_name (str): Product name
            product_features (List[str]): Product features
            target_audience (str): Target audience
            platform (str, optional): Platform (shopee, lazada, etc.). Defaults to 'shopee'.
            length (str, optional): Length of the description. Defaults to 'medium'.
            
        Returns:
            Dict: Generated product description
        """
        try:
            # Map length to token count
            length_map = {
                'short': 100,
                'medium': 200,
                'long': 400
            }
            
            max_tokens = length_map.get(length, 200)
            
            # Prepare prompt
            prompt = f"""
            Generate a product description for the following product:
            
            Product Name: {product_name}
            Product Features:
            {', '.join(product_features)}
            Target Audience: {target_audience}
            Platform: {platform}
            Length: {length}
            
            The description should be compelling, highlight key features and benefits, and be optimized for search.
            
            Format your response as JSON with the following structure:
            {{
                "title": "SEO-optimized product title",
                "short_description": "Brief product description",
                "long_description": "Detailed product description",
                "bullet_points": ["Feature 1", "Feature 2", ...],
                "keywords": ["keyword1", "keyword2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in e-commerce product descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=max_tokens * 2  # Double the tokens to account for JSON structure
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
            
            # Add metadata
            result['platform'] = platform
            result['length'] = length
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating product description: {str(e)}")
            return {'error': f"Error generating product description: {str(e)}"}
    
    def generate_video_script(self, product_name: str, product_description: str, target_audience: str, platform: str = 'tiktok', duration: str = 'short') -> Dict:
        """
        Generate video script for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str, optional): Platform (tiktok, instagram, facebook). Defaults to 'tiktok'.
            duration (str, optional): Duration of the video. Defaults to 'short'.
            
        Returns:
            Dict: Generated video script
        """
        try:
            # Map duration to seconds
            duration_map = {
                'short': 15,
                'medium': 30,
                'long': 60
            }
            
            seconds = duration_map.get(duration, 15)
            
            # Prepare prompt
            prompt = f"""
            Generate a video script for the following product:
            
            Product Name: {product_name}
            Product Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Duration: {seconds} seconds
            
            The script should be engaging, highlight key benefits, and be suitable for the platform.
            
            For TikTok, create a short, catchy script with a hook and trend elements.
            For Instagram, create a visually descriptive script with lifestyle elements.
            For Facebook, create a more informative script with clear value proposition.
            
            Format your response as JSON with the following structure:
            {{
                "hook": "Attention-grabbing opening line",
                "scenes": [
                    {{
                        "time": "0-5s",
                        "action": "Description of what happens in the scene",
                        "script": "What the presenter says",
                        "visual_elements": "Description of visual elements"
                    }},
                    ...
                ],
                "call_to_action": "Call to action at the end of the video",
                "music_mood": "Suggested mood for background music",
                "hashtags": ["hashtag1", "hashtag2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in video script creation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
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
            
            # Add metadata
            result['platform'] = platform
            result['duration'] = duration
            result['seconds'] = seconds
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating video script: {str(e)}")
            return {'error': f"Error generating video script: {str(e)}"}
    
    def generate_ad_campaign(self, product_name: str, product_description: str, target_audience: str, platforms: List[str], campaign_goal: str = 'conversions') -> Dict:
        """
        Generate a complete ad campaign for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platforms (List[str]): Platforms to include in the campaign
            campaign_goal (str, optional): Campaign goal. Defaults to 'conversions'.
            
        Returns:
            Dict: Generated ad campaign
        """
        try:
            # Prepare result
            result = {
                'campaign_name': f"{product_name} - {campaign_goal.capitalize()} Campaign",
                'campaign_goal': campaign_goal,
                'target_audience': target_audience,
                'platforms': platforms,
                'ad_creatives': {},
                'id': generate_id(),
                'created_at': datetime.now().isoformat()
            }
            
            # Generate ad copy for each platform
            for platform in platforms:
                # Generate ad copy
                ad_copy = self.generate_ad_copy(
                    product_name=product_name,
                    product_description=product_description,
                    target_audience=target_audience,
                    platform=platform
                )
                
                # Generate ad variations
                ad_variations = self.generate_ad_variations(ad_copy, variations_count=2)
                
                # Generate social media post
                social_post = self.generate_social_media_post(
                    product_name=product_name,
                    product_description=product_description,
                    target_audience=target_audience,
                    platform=platform
                )
                
                # Add to result
                result['ad_creatives'][platform] = {
                    'ad_copy': ad_copy,
                    'ad_variations': ad_variations,
                    'social_post': social_post
                }
                
                # Add video script for TikTok
                if platform == 'tiktok':
                    video_script = self.generate_video_script(
                        product_name=product_name,
                        product_description=product_description,
                        target_audience=target_audience,
                        platform=platform
                    )
                    
                    result['ad_creatives'][platform]['video_script'] = video_script
                
                # Add product description for Shopee
                if platform == 'shopee':
                    product_features = product_description.split('. ')
                    
                    product_desc = self.generate_product_description(
                        product_name=product_name,
                        product_features=product_features,
                        target_audience=target_audience,
                        platform=platform
                    )
                    
                    result['ad_creatives'][platform]['product_description'] = product_desc
            
            return result
        except Exception as e:
            logger.error(f"Error generating ad campaign: {str(e)}")
            return {'error': f"Error generating ad campaign: {str(e)}"}
    
    def analyze_ad_performance(self, ad_copy: Dict, performance_metrics: Dict) -> Dict:
        """
        Analyze ad performance and provide recommendations
        
        Args:
            ad_copy (Dict): Ad copy
            performance_metrics (Dict): Performance metrics
            
        Returns:
            Dict: Analysis and recommendations
        """
        try:
            # Extract metrics
            impressions = performance_metrics.get('impressions', 0)
            clicks = performance_metrics.get('clicks', 0)
            conversions = performance_metrics.get('conversions', 0)
            
            # Calculate CTR and CVR
            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            cvr = (conversions / clicks * 100) if clicks > 0 else 0
            
            # Prepare prompt
            prompt = f"""
            Analyze the performance of the following ad copy:
            
            Headline: {ad_copy.get('headline', '')}
            Main Text: {ad_copy.get('main_text', '')}
            Call to Action: {ad_copy.get('call_to_action', '')}
            
            Performance Metrics:
            Impressions: {impressions}
            Clicks: {clicks}
            Conversions: {conversions}
            CTR: {ctr:.2f}%
            CVR: {cvr:.2f}%
            
            Provide an analysis of the ad performance and recommendations for improvement.
            
            Format your response as JSON with the following structure:
            {{
                "analysis": "Analysis of the ad performance",
                "strengths": ["Strength 1", "Strength 2", ...],
                "weaknesses": ["Weakness 1", "Weakness 2", ...],
                "recommendations": [
                    {{
                        "type": "headline",
                        "description": "Recommendation for headline improvement",
                        "suggestion": "Suggested headline"
                    }},
                    ...
                ]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in ad performance analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=500
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
            
            # Add metrics
            result['metrics'] = {
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'ctr': ctr,
                'cvr': cvr
            }
            
            # Add metadata
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error analyzing ad performance: {str(e)}")
            return {'error': f"Error analyzing ad performance: {str(e)}"}
    
    def optimize_ad_copy(self, ad_copy: Dict, performance_metrics: Dict = None) -> Dict:
        """
        Optimize ad copy based on performance metrics
        
        Args:
            ad_copy (Dict): Ad copy
            performance_metrics (Dict, optional): Performance metrics. Defaults to None.
            
        Returns:
            Dict: Optimized ad copy
        """
        try:
            # Extract ad copy
            headline = ad_copy.get('headline', '')
            main_text = ad_copy.get('main_text', '')
            call_to_action = ad_copy.get('call_to_action', '')
            platform = ad_copy.get('platform', 'facebook')
            
            # Prepare prompt
            prompt = f"""
            Optimize the following ad copy:
            
            Headline: {headline}
            Main Text: {main_text}
            Call to Action: {call_to_action}
            Platform: {platform}
            """
            
            if performance_metrics:
                # Extract metrics
                impressions = performance_metrics.get('impressions', 0)
                clicks = performance_metrics.get('clicks', 0)
                conversions = performance_metrics.get('conversions', 0)
                
                # Calculate CTR and CVR
                ctr = (clicks / impressions * 100) if impressions > 0 else 0
                cvr = (conversions / clicks * 100) if clicks > 0 else 0
                
                prompt += f"""
                
                Performance Metrics:
                Impressions: {impressions}
                Clicks: {clicks}
                Conversions: {conversions}
                CTR: {ctr:.2f}%
                CVR: {cvr:.2f}%
                """
            
            prompt += """
            
            Optimize the ad copy to improve performance. Make it more compelling, engaging, and effective.
            
            Format your response as JSON with the following structure:
            {
                "headline": "Optimized headline",
                "main_text": "Optimized main text",
                "call_to_action": "Optimized call to action",
                "changes": {
                    "headline": "Description of changes made to headline",
                    "main_text": "Description of changes made to main text",
                    "call_to_action": "Description of changes made to call to action"
                }
            }
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in ad copy optimization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
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
            
            # Add metadata
            result['platform'] = platform
            result['original_id'] = ad_copy.get('id')
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error optimizing ad copy: {str(e)}")
            return {'error': f"Error optimizing ad copy: {str(e)}"}
    
    def generate_ab_test_variations(self, ad_copy: Dict, elements_to_test: List[str] = ['headline', 'main_text', 'call_to_action'], variations_per_element: int = 2) -> Dict:
        """
        Generate A/B test variations for ad copy
        
        Args:
            ad_copy (Dict): Ad copy
            elements_to_test (List[str], optional): Elements to test. Defaults to ['headline', 'main_text', 'call_to_action'].
            variations_per_element (int, optional): Number of variations per element. Defaults to 2.
            
        Returns:
            Dict: A/B test variations
        """
        try:
            # Extract ad copy
            headline = ad_copy.get('headline', '')
            main_text = ad_copy.get('main_text', '')
            call_to_action = ad_copy.get('call_to_action', '')
            platform = ad_copy.get('platform', 'facebook')
            
            # Prepare prompt
            prompt = f"""
            Generate A/B test variations for the following ad copy:
            
            Headline: {headline}
            Main Text: {main_text}
            Call to Action: {call_to_action}
            Platform: {platform}
            
            Elements to test: {', '.join(elements_to_test)}
            Variations per element: {variations_per_element}
            
            For each element, generate variations that test different approaches, tones, or value propositions.
            
            Format your response as JSON with the following structure:
            {{
                "headline_variations": [
                    {{
                        "text": "Headline variation 1",
                        "approach": "Description of the approach"
                    }},
                    ...
                ],
                "main_text_variations": [
                    {{
                        "text": "Main text variation 1",
                        "approach": "Description of the approach"
                    }},
                    ...
                ],
                "call_to_action_variations": [
                    {{
                        "text": "Call to action variation 1",
                        "approach": "Description of the approach"
                    }},
                    ...
                ]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in A/B testing for ads."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
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
            
            # Add metadata
            result['platform'] = platform
            result['original_ad'] = {
                'headline': headline,
                'main_text': main_text,
                'call_to_action': call_to_action
            }
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating A/B test variations: {str(e)}")
            return {'error': f"Error generating A/B test variations: {str(e)}"}
    
    def generate_seasonal_ad_copy(self, product_name: str, product_description: str, target_audience: str, platform: str, season: str) -> Dict:
        """
        Generate seasonal ad copy for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            season (str): Season or holiday (e.g., Christmas, New Year, Summer)
            
        Returns:
            Dict: Generated seasonal ad copy
        """
        try:
            # Prepare prompt
            prompt = f"""
            Generate seasonal ad copy for the following product:
            
            Product Name: {product_name}
            Product Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Season/Holiday: {season}
            
            The ad copy should be compelling, highlight key benefits, include a call to action, and be themed around the specified season or holiday.
            
            Format your response as JSON with the following structure:
            {{
                "headline": "Compelling headline",
                "main_text": "Main ad copy text",
                "call_to_action": "Call to action text",
                "seasonal_elements": ["Element 1", "Element 2", ...],
                "keywords": ["keyword1", "keyword2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in seasonal ad copy generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
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
            
            # Add metadata
            result['platform'] = platform
            result['season'] = season
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating seasonal ad copy: {str(e)}")
            return {'error': f"Error generating seasonal ad copy: {str(e)}"}
    
    def generate_localized_ad_copy(self, product_name: str, product_description: str, target_audience: str, platform: str, locale: str) -> Dict:
        """
        Generate localized ad copy for a product
        
        Args:
            product_name (str): Product name
            product_description (str): Product description
            target_audience (str): Target audience
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            locale (str): Locale (e.g., th-TH, en-US)
            
        Returns:
            Dict: Generated localized ad copy
        """
        try:
            # Prepare prompt
            prompt = f"""
            Generate localized ad copy for the following product:
            
            Product Name: {product_name}
            Product Description: {product_description}
            Target Audience: {target_audience}
            Platform: {platform}
            Locale: {locale}
            
            The ad copy should be compelling, highlight key benefits, include a call to action, and be localized for the specified locale.
            
            Format your response as JSON with the following structure:
            {{
                "headline": "Compelling headline",
                "main_text": "Main ad copy text",
                "call_to_action": "Call to action text",
                "cultural_elements": ["Element 1", "Element 2", ...],
                "keywords": ["keyword1", "keyword2", ...]
            }}
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI marketing expert specializing in localized ad copy generation."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
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
            
            # Add metadata
            result['platform'] = platform
            result['locale'] = locale
            result['id'] = generate_id()
            result['created_at'] = datetime.now().isoformat()
            
            return result
        except Exception as e:
            logger.error(f"Error generating localized ad copy: {str(e)}")
            return {'error': f"Error generating localized ad copy: {str(e)}"}
