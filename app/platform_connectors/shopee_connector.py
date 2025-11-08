"""
AdGenius AI Backend - Shopee API Connector
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

class ShopeeConnector:
    """Shopee API connector"""
    
    def __init__(self):
        """Initialize Shopee connector"""
        self.partner_id = os.getenv('SHOPEE_PARTNER_ID')
        self.partner_key = os.getenv('SHOPEE_PARTNER_KEY')
        self.api_base_url = os.getenv('SHOPEE_API_BASE_URL', 'https://partner.shopeemobile.com/api/v2')
        self.initialized = False
    
    def initialize(self, access_token: str, shop_id: str):
        """
        Initialize Shopee API
        
        Args:
            access_token (str): Access token
            shop_id (str): Shop ID
        """
        try:
            self.access_token = access_token
            self.shop_id = shop_id
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize Shopee API: {str(e)}")
            self.initialized = False
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """
        Make API request to Shopee
        
        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            params (Dict, optional): Query parameters
            data (Dict, optional): Request body
            
        Returns:
            Dict: API response
        """
        if not self.initialized:
            return {'error': 'Shopee API not initialized'}
        
        # Build URL
        url = f"{self.api_base_url}{endpoint}"
        
        # Add common parameters
        if params is None:
            params = {}
        
        params['partner_id'] = self.partner_id
        params['timestamp'] = int(time.time())
        params['access_token'] = self.access_token
        params['shop_id'] = self.shop_id
        
        # Generate signature
        base_string = f"{self.partner_id}{endpoint}{params['timestamp']}{self.access_token}{self.shop_id}"
        signature = hmac.new(
            self.partner_key.encode(),
            base_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        params['sign'] = signature
        
        try:
            # Make request
            if method == 'GET':
                response = requests.get(url, params=params)
            elif method == 'POST':
                response = requests.post(url, json=data, params=params)
            else:
                return {'error': f"Unsupported HTTP method: {method}"}
            
            # Parse response
            response_data = response.json()
            
            # Check for errors
            if response.status_code != 200 or response_data.get('error') is not None:
                error_message = response_data.get('message', 'Unknown error')
                logger.error(f"Shopee API error: {error_message}")
                return {'error': f"Shopee API error: {error_message}"}
            
            return response_data.get('response', {})
        except Exception as e:
            logger.error(f"Error making Shopee API request: {str(e)}")
            return {'error': f"Error making Shopee API request: {str(e)}"}
    
    def get_shop_info(self) -> Dict:
        """
        Get shop information
        
        Returns:
            Dict: Shop information
        """
        try:
            # Get shop info
            response = self._make_request('GET', '/shop/get_shop_info')
            
            if 'error' in response:
                return response
            
            return response
        except Exception as e:
            logger.error(f"Error getting shop info: {str(e)}")
            return {'error': f"Error getting shop info: {str(e)}"}
    
    def get_products(self, offset: int = 0, limit: int = 100) -> List[Dict]:
        """
        Get products
        
        Args:
            offset (int, optional): Offset. Defaults to 0.
            limit (int, optional): Limit. Defaults to 100.
            
        Returns:
            List[Dict]: Products
        """
        try:
            # Get products
            data = {
                'offset': offset,
                'page_size': limit,
                'item_status': 'NORMAL'
            }
            
            response = self._make_request('GET', '/product/get_item_list', params=data)
            
            if 'error' in response:
                return response
            
            # Format products
            result = []
            
            for item in response.get('item', []):
                result.append({
                    'id': item.get('item_id'),
                    'name': item.get('item_name'),
                    'category_id': item.get('category_id'),
                    'price': item.get('price'),
                    'stock': item.get('stock'),
                    'sales': item.get('sold'),
                    'image': item.get('image')
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting products: {str(e)}")
            return {'error': f"Error getting products: {str(e)}"}
    
    def get_product_details(self, product_id: str) -> Dict:
        """
        Get product details
        
        Args:
            product_id (str): Product ID
            
        Returns:
            Dict: Product details
        """
        try:
            # Get product details
            data = {
                'item_id_list': [product_id]
            }
            
            response = self._make_request('GET', '/product/get_item_base_info', params=data)
            
            if 'error' in response:
                return response
            
            # Get first product
            if not response.get('item_list'):
                return {'error': 'Product not found'}
            
            product = response.get('item_list')[0]
            
            # Get product categories
            category_response = self._make_request('GET', '/product/get_category', params={'category_id': product.get('category_id')})
            
            category_name = ''
            
            if 'error' not in category_response and category_response.get('category_list'):
                category = category_response.get('category_list')[0]
                category_name = category.get('category_name', '')
            
            # Format product
            return {
                'id': product.get('item_id'),
                'name': product.get('item_name'),
                'description': product.get('description'),
                'category_id': product.get('category_id'),
                'category_name': category_name,
                'price': product.get('price'),
                'stock': product.get('stock'),
                'sales': product.get('sold'),
                'images': product.get('image', {}).get('image_url_list', []),
                'attributes': product.get('attribute_list', []),
                'rating': product.get('rating_star', 0),
                'rating_count': product.get('rating_count', 0)
            }
        except Exception as e:
            logger.error(f"Error getting product details: {str(e)}")
            return {'error': f"Error getting product details: {str(e)}"}
    
    def get_product_categories(self) -> List[Dict]:
        """
        Get product categories
        
        Returns:
            List[Dict]: Product categories
        """
        try:
            # Get categories
            response = self._make_request('GET', '/product/get_category')
            
            if 'error' in response:
                return response
            
            # Format categories
            result = []
            
            for category in response.get('category_list', []):
                result.append({
                    'id': category.get('category_id'),
                    'name': category.get('category_name'),
                    'parent_id': category.get('parent_category_id')
                })
            
            return result
        except Exception as e:
            logger.error(f"Error getting product categories: {str(e)}")
            return {'error': f"Error getting product categories: {str(e)}"}
    
    def get_product_performance(self, product_id: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get product performance
        
        Args:
            product_id (str): Product ID
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Product performance
        """
        try:
            # Format dates
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Get product performance
            data = {
                'item_id': product_id,
                'start_time': int(start_date.timestamp()),
                'end_time': int(end_date.timestamp())
            }
            
            response = self._make_request('GET', '/product/get_item_promotion', params=data)
            
            if 'error' in response:
                return response
            
            # Get product details
            product_details = self.get_product_details(product_id)
            
            if 'error' in product_details:
                return product_details
            
            # Get product orders
            orders_data = {
                'time_range_field': 'create_time',
                'time_from': int(start_date.timestamp()),
                'time_to': int(end_date.timestamp()),
                'page_size': 100
            }
            
            orders_response = self._make_request('GET', '/order/get_order_list', params=orders_data)
            
            # Calculate metrics
            total_views = 0
            total_sales = 0
            total_revenue = 0.0
            
            # Process promotion data
            for promotion in response.get('item_promotion_list', []):
                total_views += promotion.get('view_count', 0)
                total_sales += promotion.get('sold_count', 0)
                total_revenue += promotion.get('sold_count', 0) * product_details.get('price', 0)
            
            # Process orders
            if 'error' not in orders_response:
                for order in orders_response.get('order_list', []):
                    for item in order.get('item_list', []):
                        if item.get('item_id') == product_id:
                            total_sales += item.get('model_quantity_purchased', 0)
                            total_revenue += item.get('model_quantity_purchased', 0) * item.get('model_original_price', 0)
            
            # Calculate conversion rate
            conversion_rate = (total_sales / total_views * 100) if total_views > 0 else 0
            
            return {
                'product_id': product_id,
                'product_name': product_details.get('name'),
                'total_views': total_views,
                'total_sales': total_sales,
                'total_revenue': total_revenue,
                'conversion_rate': conversion_rate,
                'average_price': product_details.get('price', 0),
                'rating': product_details.get('rating', 0),
                'rating_count': product_details.get('rating_count', 0)
            }
        except Exception as e:
            logger.error(f"Error getting product performance: {str(e)}")
            return {'error': f"Error getting product performance: {str(e)}"}
    
    def get_shop_performance(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get shop performance
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Shop performance
        """
        try:
            # Format dates
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            # Get shop performance
            data = {
                'start_time': int(start_date.timestamp()),
                'end_time': int(end_date.timestamp())
            }
            
            response = self._make_request('GET', '/shop/get_shop_performance', params=data)
            
            if 'error' in response:
                return response
            
            # Get shop info
            shop_info = self.get_shop_info()
            
            if 'error' in shop_info:
                return shop_info
            
            # Get orders
            orders_data = {
                'time_range_field': 'create_time',
                'time_from': int(start_date.timestamp()),
                'time_to': int(end_date.timestamp()),
                'page_size': 100
            }
            
            orders_response = self._make_request('GET', '/order/get_order_list', params=orders_data)
            
            # Calculate metrics
            total_views = response.get('shop_views', 0)
            total_orders = 0
            total_revenue = 0.0
            
            # Process orders
            if 'error' not in orders_response:
                for order in orders_response.get('order_list', []):
                    total_orders += 1
                    total_revenue += order.get('total_amount', 0)
            
            # Calculate conversion rate
            conversion_rate = (total_orders / total_views * 100) if total_views > 0 else 0
            
            return {
                'shop_id': self.shop_id,
                'shop_name': shop_info.get('shop_name'),
                'total_views': total_views,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'conversion_rate': conversion_rate,
                'average_order_value': (total_revenue / total_orders) if total_orders > 0 else 0,
                'rating': shop_info.get('rating_star', 0),
                'rating_count': shop_info.get('rating_count', 0)
            }
        except Exception as e:
            logger.error(f"Error getting shop performance: {str(e)}")
            return {'error': f"Error getting shop performance: {str(e)}"}
    
    def create_discount(self, product_id: str, discount_percentage: float, start_date: datetime, end_date: datetime) -> Dict:
        """
        Create discount
        
        Args:
            product_id (str): Product ID
            discount_percentage (float): Discount percentage
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Result
        """
        try:
            # Get product details
            product_details = self.get_product_details(product_id)
            
            if 'error' in product_details:
                return product_details
            
            # Calculate discount price
            original_price = product_details.get('price', 0)
            discount_price = original_price * (1 - discount_percentage / 100)
            
            # Create discount
            data = {
                'discount_name': f"AdGenius AI Discount {discount_percentage}%",
                'start_time': int(start_date.timestamp()),
                'end_time': int(end_date.timestamp()),
                'items': [
                    {
                        'item_id': product_id,
                        'variations': [
                            {
                                'variation_id': 0,  # 0 means all variations
                                'variation_promotion_price': discount_price
                            }
                        ]
                    }
                ]
            }
            
            response = self._make_request('POST', '/discount/add_discount', data=data)
            
            if 'error' in response:
                return response
            
            return {
                'discount_id': response.get('discount_id'),
                'product_id': product_id,
                'original_price': original_price,
                'discount_price': discount_price,
                'discount_percentage': discount_percentage,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        except Exception as e:
            logger.error(f"Error creating discount: {str(e)}")
            return {'error': f"Error creating discount: {str(e)}"}
    
    def create_promotion(self, product_id: str, promotion_type: str, start_date: datetime, end_date: datetime) -> Dict:
        """
        Create promotion
        
        Args:
            product_id (str): Product ID
            promotion_type (str): Promotion type
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Result
        """
        try:
            # Map promotion type
            type_mapping = {
                'flash_sale': 'flash_sale',
                'daily_discover': 'daily_discover',
                'welcome_package': 'welcome_package',
                'shop_top_picks': 'shop_top_picks'
            }
            
            shopee_promotion_type = type_mapping.get(promotion_type, 'daily_discover')
            
            # Create promotion
            data = {
                'item_id': product_id,
                'promotion_type': shopee_promotion_type,
                'start_time': int(start_date.timestamp()),
                'end_time': int(end_date.timestamp())
            }
            
            response = self._make_request('POST', '/product/add_item_promotion', data=data)
            
            if 'error' in response:
                return response
            
            return {
                'promotion_id': response.get('promotion_id'),
                'product_id': product_id,
                'promotion_type': promotion_type,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            }
        except Exception as e:
            logger.error(f"Error creating promotion: {str(e)}")
            return {'error': f"Error creating promotion: {str(e)}"}
    
    def boost_product(self, product_id: str) -> Dict:
        """
        Boost product
        
        Args:
            product_id (str): Product ID
            
        Returns:
            Dict: Result
        """
        try:
            # Boost product
            data = {
                'item_id': product_id
            }
            
            response = self._make_request('POST', '/product/boost_item', data=data)
            
            if 'error' in response:
                return response
            
            return {
                'product_id': product_id,
                'boost_status': response.get('boost_status'),
                'boost_expires_at': response.get('boost_expires_at')
            }
        except Exception as e:
            logger.error(f"Error boosting product: {str(e)}")
            return {'error': f"Error boosting product: {str(e)}"}
    
    def get_product_recommendations(self, product_id: str) -> List[Dict]:
        """
        Get product recommendations
        
        Args:
            product_id (str): Product ID
            
        Returns:
            List[Dict]: Product recommendations
        """
        try:
            # Get product details
            product_details = self.get_product_details(product_id)
            
            if 'error' in product_details:
                return product_details
            
            # Get similar products
            data = {
                'category_id': product_details.get('category_id'),
                'offset': 0,
                'page_size': 10
            }
            
            response = self._make_request('GET', '/product/get_item_list', params=data)
            
            if 'error' in response:
                return response
            
            # Format recommendations
            result = []
            
            for item in response.get('item', []):
                if item.get('item_id') != product_id:  # Exclude the original product
                    result.append({
                        'id': item.get('item_id'),
                        'name': item.get('item_name'),
                        'category_id': item.get('category_id'),
                        'price': item.get('price'),
                        'stock': item.get('stock'),
                        'sales': item.get('sold'),
                        'image': item.get('image')
                    })
            
            return result
        except Exception as e:
            logger.error(f"Error getting product recommendations: {str(e)}")
            return {'error': f"Error getting product recommendations: {str(e)}"}
    
    def get_product_keywords(self, product_id: str) -> List[Dict]:
        """
        Get product keywords
        
        Args:
            product_id (str): Product ID
            
        Returns:
            List[Dict]: Product keywords
        """
        try:
            # Get product details
            product_details = self.get_product_details(product_id)
            
            if 'error' in product_details:
                return product_details
            
            # Get category keywords
            data = {
                'category_id': product_details.get('category_id')
            }
            
            response = self._make_request('GET', '/product/get_category_keywords', params=data)
            
            if 'error' in response:
                return response
            
            # Format keywords
            result = []
            
            for keyword in response.get('keywords', []):
                result.append({
                    'keyword': keyword.get('keyword'),
                    'search_volume': keyword.get('search_volume', 0),
                    'relevance': keyword.get('relevance', 0)
                })
            
            # Sort by search volume
            result.sort(key=lambda x: x.get('search_volume', 0), reverse=True)
            
            return result
        except Exception as e:
            logger.error(f"Error getting product keywords: {str(e)}")
            return {'error': f"Error getting product keywords: {str(e)}"}
    
    def optimize_product_listing(self, product_id: str) -> Dict:
        """
        Optimize product listing
        
        Args:
            product_id (str): Product ID
            
        Returns:
            Dict: Optimization recommendations
        """
        try:
            # Get product details
            product_details = self.get_product_details(product_id)
            
            if 'error' in product_details:
                return product_details
            
            # Get product keywords
            keywords = self.get_product_keywords(product_id)
            
            if isinstance(keywords, dict) and 'error' in keywords:
                keywords = []
            
            # Get product performance
            performance = self.get_product_performance(
                product_id,
                datetime.now() - timedelta(days=30),
                datetime.now()
            )
            
            if isinstance(performance, dict) and 'error' in performance:
                performance = {
                    'total_views': 0,
                    'total_sales': 0,
                    'conversion_rate': 0
                }
            
            # Generate recommendations
            recommendations = []
            
            # Check title
            title = product_details.get('name', '')
            
            if len(title) < 30:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'title',
                    'priority': 'high',
                    'description': 'Your product title is too short. Consider adding more relevant keywords to improve visibility.',
                    'expected_impact': 'Longer titles with relevant keywords can improve search visibility.'
                })
            
            # Check if title contains top keywords
            if keywords:
                top_keywords = [keyword.get('keyword') for keyword in keywords[:5]]
                missing_keywords = []
                
                for keyword in top_keywords:
                    if keyword.lower() not in title.lower():
                        missing_keywords.append(keyword)
                
                if missing_keywords:
                    recommendations.append({
                        'id': generate_id(),
                        'type': 'title',
                        'priority': 'medium',
                        'description': f"Consider adding these high-volume keywords to your title: {', '.join(missing_keywords)}",
                        'expected_impact': 'Including high-volume keywords can improve search visibility.'
                    })
            
            # Check description
            description = product_details.get('description', '')
            
            if len(description) < 100:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'description',
                    'priority': 'medium',
                    'description': 'Your product description is too short. Consider adding more details about features, benefits, and usage.',
                    'expected_impact': 'Detailed descriptions can improve conversion rates.'
                })
            
            # Check images
            images = product_details.get('images', [])
            
            if len(images) < 3:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'images',
                    'priority': 'high',
                    'description': 'Add more product images from different angles to showcase your product better.',
                    'expected_impact': 'More images can increase buyer confidence and conversion rates.'
                })
            
            # Check price
            if performance.get('conversion_rate', 0) < 2.0:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'price',
                    'priority': 'medium',
                    'description': 'Your conversion rate is low. Consider testing a lower price point or offering discounts.',
                    'expected_impact': 'Price adjustments can increase conversion rates and overall revenue.'
                })
            
            # Check attributes
            attributes = product_details.get('attributes', [])
            
            if len(attributes) < 5:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'attributes',
                    'priority': 'low',
                    'description': 'Add more product attributes to provide detailed specifications.',
                    'expected_impact': 'Detailed attributes can improve search visibility and conversion rates.'
                })
            
            return {
                'product_id': product_id,
                'product_name': product_details.get('name'),
                'current_performance': {
                    'views': performance.get('total_views', 0),
                    'sales': performance.get('total_sales', 0),
                    'conversion_rate': performance.get('conversion_rate', 0)
                },
                'top_keywords': keywords[:10] if keywords else [],
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error optimizing product listing: {str(e)}")
            return {'error': f"Error optimizing product listing: {str(e)}"}
    
    def publish_campaign(self, campaign: Campaign) -> Dict:
        """
        Publish campaign to Shopee
        
        Args:
            campaign (Campaign): Campaign
            
        Returns:
            Dict: Result with platform ID
        """
        # Get user
        user = campaign.user
        
        # Find Shopee account
        shopee_account = None
        
        for account in user.platform_accounts:
            if account.platform == 'shopee':
                shopee_account = account
                break
        
        if not shopee_account:
            return {'error': 'No Shopee account found'}
        
        # Initialize API
        self.initialize(shopee_account.access_token, shopee_account.account_id)
        
        if not self.initialized:
            return {'error': 'Failed to initialize Shopee API'}
        
        try:
            # Get products
            products = self.get_products()
            
            if isinstance(products, dict) and 'error' in products:
                return products
            
            # Create promotions for each product
            promotion_ids = []
            
            for product in products[:10]:  # Limit to 10 products
                # Create discount
                discount_result = self.create_discount(
                    product_id=product.get('id'),
                    discount_percentage=10,  # 10% discount
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=7)
                )
                
                if isinstance(discount_result, dict) and 'error' not in discount_result:
                    promotion_ids.append(discount_result.get('discount_id'))
                
                # Create promotion
                promotion_result = self.create_promotion(
                    product_id=product.get('id'),
                    promotion_type='daily_discover',
                    start_date=datetime.now(),
                    end_date=datetime.now() + timedelta(days=7)
                )
                
                if isinstance(promotion_result, dict) and 'error' not in promotion_result:
                    promotion_ids.append(promotion_result.get('promotion_id'))
                
                # Boost product
                self.boost_product(product.get('id'))
            
            # Save campaign
            campaign.platform_campaign_id = f"shopee_{int(time.time())}"
            campaign.save()
            
            return {
                'platform_id': campaign.platform_campaign_id,
                'promotion_ids': promotion_ids,
                'product_count': len(products[:10])
            }
        except Exception as e:
            logger.error(f"Error publishing campaign: {str(e)}")
            return {'error': f"Error publishing campaign: {str(e)}"}
    
    def get_campaign_analytics(self, start_date: datetime, end_date: datetime) -> Dict:
        """
        Get campaign analytics
        
        Args:
            start_date (datetime): Start date
            end_date (datetime): End date
            
        Returns:
            Dict: Campaign analytics
        """
        try:
            # Get shop performance
            shop_performance = self.get_shop_performance(start_date, end_date)
            
            if 'error' in shop_performance:
                return shop_performance
            
            # Get products
            products = self.get_products()
            
            if isinstance(products, dict) and 'error' in products:
                return products
            
            # Get product performance
            product_performance = []
            
            for product in products[:10]:  # Limit to 10 products
                performance = self.get_product_performance(product.get('id'), start_date, end_date)
                
                if isinstance(performance, dict) and 'error' not in performance:
                    product_performance.append(performance)
            
            # Calculate metrics
            total_views = shop_performance.get('total_views', 0)
            total_orders = shop_performance.get('total_orders', 0)
            total_revenue = shop_performance.get('total_revenue', 0)
            
            # Calculate conversion rate
            conversion_rate = (total_orders / total_views * 100) if total_views > 0 else 0
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                shop_performance=shop_performance,
                product_performance=product_performance
            )
            
            return {
                'total_views': total_views,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'conversion_rate': conversion_rate,
                'average_order_value': shop_performance.get('average_order_value', 0),
                'product_performance': product_performance,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error getting campaign analytics: {str(e)}")
            return {'error': f"Error getting campaign analytics: {str(e)}"}
    
    def _generate_recommendations(self, shop_performance: Dict, product_performance: List[Dict]) -> List[Dict]:
        """
        Generate recommendations
        
        Args:
            shop_performance (Dict): Shop performance
            product_performance (List[Dict]): Product performance
            
        Returns:
            List[Dict]: Recommendations
        """
        recommendations = []
        
        # Check conversion rate
        if shop_performance.get('conversion_rate', 0) < 2.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'shop',
                'priority': 'high',
                'description': 'Your shop conversion rate is low. Consider improving product listings, offering discounts, or enhancing shop reputation.',
                'expected_impact': 'Increasing conversion rate directly impacts your revenue.'
            })
        
        # Check average order value
        if shop_performance.get('average_order_value', 0) < 20.0:
            recommendations.append({
                'id': generate_id(),
                'type': 'shop',
                'priority': 'medium',
                'description': 'Your average order value is low. Consider bundling products, offering volume discounts, or upselling complementary products.',
                'expected_impact': 'Increasing average order value can boost revenue without increasing traffic.'
            })
        
        # Check product performance
        if product_performance:
            # Find best and worst performing products
            best_product = max(product_performance, key=lambda x: x.get('conversion_rate', 0))
            worst_product = min(product_performance, key=lambda x: x.get('conversion_rate', 0))
            
            # If there's a significant difference
            if best_product.get('conversion_rate', 0) > worst_product.get('conversion_rate', 0) * 2:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'product',
                    'priority': 'medium',
                    'description': f"There's a significant performance gap between your products. Consider optimizing the listing for '{worst_product.get('product_name')}' based on what works for '{best_product.get('product_name')}'.",
                    'expected_impact': 'Improving low-performing products can increase overall shop performance.'
                })
            
            # Check for low-performing products
            low_performing_products = []
            
            for product in product_performance:
                if product.get('conversion_rate', 0) < 1.0:
                    low_performing_products.append(product.get('product_name'))
            
            if low_performing_products:
                recommendations.append({
                    'id': generate_id(),
                    'type': 'product',
                    'priority': 'high',
                    'description': f"The following products have low conversion rates: {', '.join(low_performing_products[:3])}. Consider optimizing listings or offering discounts.",
                    'expected_impact': 'Improving conversion rates for these products can significantly boost overall performance.'
                })
        
        # Shopee-specific recommendations
        recommendations.append({
            'id': generate_id(),
            'type': 'shop',
            'priority': 'low',
            'description': 'Participate in Shopee campaigns and promotions to increase visibility and sales.',
            'expected_impact': 'Shopee campaigns can drive significant traffic and sales.'
        })
        
        recommendations.append({
            'id': generate_id(),
            'type': 'product',
            'priority': 'medium',
            'description': 'Use Shopee Boost feature for your best-selling products to increase visibility.',
            'expected_impact': 'Boosted products appear higher in search results, driving more traffic and sales.'
        })
        
        return recommendations
