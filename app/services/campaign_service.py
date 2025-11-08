"""
AdGenius AI Backend - Campaign Service
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from app.models.user import User
from app.models.campaign import (
    Campaign, Budget, Schedule, Targeting, Creative, 
    Performance, Optimization
)
from app.platform_connectors.facebook_connector import FacebookConnector
from app.platform_connectors.instagram_connector import InstagramConnector
from app.platform_connectors.tiktok_connector import TikTokConnector
from app.platform_connectors.shopee_connector import ShopeeConnector
from app.ai_modules.targeting import TargetingAI
from app.ai_modules.creative import CreativeAI
from app.ai_modules.optimization import OptimizationAI

class CampaignService:
    """Campaign service"""
    
    def __init__(self):
        """Initialize campaign service"""
        self.facebook_connector = FacebookConnector()
        self.instagram_connector = InstagramConnector()
        self.tiktok_connector = TikTokConnector()
        self.shopee_connector = ShopeeConnector()
        self.targeting_ai = TargetingAI()
        self.creative_ai = CreativeAI()
        self.optimization_ai = OptimizationAI()
    
    def get_campaigns(self, user_id: str, page: int = 1, per_page: int = 10, 
                     platform: Optional[str] = None, status: Optional[str] = None) -> Dict:
        """
        Get campaigns for user
        
        Args:
            user_id (str): User ID
            page (int, optional): Page number. Defaults to 1.
            per_page (int, optional): Items per page. Defaults to 10.
            platform (Optional[str], optional): Filter by platform. Defaults to None.
            status (Optional[str], optional): Filter by status. Defaults to None.
            
        Returns:
            Dict: Campaigns with pagination
        """
        # Create query
        query = {'user': user_id}
        
        # Add filters
        if platform:
            query['platform'] = platform
        
        if status:
            query['status'] = status
        
        # Get total count
        total = Campaign.objects(**query).count()
        
        # Calculate pagination
        skip = (page - 1) * per_page
        total_pages = (total + per_page - 1) // per_page if total > 0 else 0
        
        # Get campaigns
        campaigns = Campaign.objects(**query).order_by('-created_at').skip(skip).limit(per_page)
        
        # Convert to dictionaries
        campaign_list = [campaign.to_dict() for campaign in campaigns]
        
        return {
            'campaigns': campaign_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'total_pages': total_pages
            }
        }
    
    def get_campaign_by_id(self, campaign_id: str, user_id: str) -> Optional[Dict]:
        """
        Get campaign by ID
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            
        Returns:
            Optional[Dict]: Campaign dictionary or None
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return None
        
        return campaign.to_dict()
    
    def create_campaign(self, user_id: str, name: str, platform: str, objective: str, 
                       budget: Optional[Dict] = None, start_date: Optional[str] = None, 
                       end_date: Optional[str] = None, targeting: Optional[Dict] = None, 
                       creatives: Optional[List[Dict]] = None) -> Dict:
        """
        Create a new campaign
        
        Args:
            user_id (str): User ID
            name (str): Campaign name
            platform (str): Platform (facebook, instagram, tiktok, shopee)
            objective (str): Campaign objective
            budget (Optional[Dict], optional): Budget details. Defaults to None.
            start_date (Optional[str], optional): Start date. Defaults to None.
            end_date (Optional[str], optional): End date. Defaults to None.
            targeting (Optional[Dict], optional): Targeting details. Defaults to None.
            creatives (Optional[List[Dict]], optional): Creatives. Defaults to None.
            
        Returns:
            Dict: Created campaign
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Create campaign
        campaign = Campaign(
            user=user,
            name=name,
            platform=platform,
            objective=objective
        )
        
        # Set budget if provided
        if budget:
            campaign_budget = Budget(
                amount=budget.get('amount', 0),
                currency=budget.get('currency', 'THB'),
                type=budget.get('type', 'daily')
            )
            campaign_budget.calculate_remaining()
            campaign.budget = campaign_budget
        
        # Set schedule if start_date provided
        if start_date:
            campaign_schedule = Schedule(
                start_date=datetime.fromisoformat(start_date)
            )
            
            if end_date:
                campaign_schedule.end_date = datetime.fromisoformat(end_date)
            
            campaign.schedule = campaign_schedule
        
        # Set targeting if provided
        if targeting:
            campaign_targeting = Targeting(
                age_min=targeting.get('age_min', 18),
                age_max=targeting.get('age_max', 65),
                genders=targeting.get('genders', ['all']),
                locations=targeting.get('locations', []),
                interests=targeting.get('interests', []),
                behaviors=targeting.get('behaviors', []),
                custom_audiences=targeting.get('custom_audiences', []),
                excluded_audiences=targeting.get('excluded_audiences', []),
                device_platforms=targeting.get('device_platforms', ['mobile', 'desktop']),
                platforms=targeting.get('platforms', [platform]),
                placements=targeting.get('placements', []),
                optimization_goal=targeting.get('optimization_goal', '')
            )
            campaign.targeting = campaign_targeting
        else:
            # Create default targeting
            campaign_targeting = Targeting(
                age_min=18,
                age_max=65,
                genders=['all'],
                device_platforms=['mobile', 'desktop'],
                platforms=[platform]
            )
            campaign.targeting = campaign_targeting
        
        # Add creatives if provided
        if creatives:
            for creative_data in creatives:
                creative = Creative(
                    id=str(uuid.uuid4()),
                    type=creative_data.get('type', 'image'),
                    name=creative_data.get('name', f"Creative {len(campaign.creatives) + 1}"),
                    primary_text=creative_data.get('primary_text', ''),
                    headline=creative_data.get('headline', ''),
                    description=creative_data.get('description', ''),
                    call_to_action=creative_data.get('call_to_action', ''),
                    media_urls=creative_data.get('media_urls', []),
                    thumbnail_url=creative_data.get('thumbnail_url', ''),
                    destination_url=creative_data.get('destination_url', ''),
                    tracking_url=creative_data.get('tracking_url', ''),
                    ai_generated=creative_data.get('ai_generated', False),
                    ai_prompt=creative_data.get('ai_prompt', '')
                )
                campaign.creatives.append(creative)
        
        # Save campaign
        campaign.save()
        
        return campaign.to_dict()
    
    def update_campaign(self, campaign_id: str, user_id: str, **kwargs) -> Optional[Dict]:
        """
        Update campaign
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            **kwargs: Campaign attributes to update
            
        Returns:
            Optional[Dict]: Updated campaign or None
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return None
        
        # Update simple attributes
        for key, value in kwargs.items():
            if key in ['name', 'objective', 'notes', 'tags', 'industry', 'product_category']:
                setattr(campaign, key, value)
        
        # Update budget
        if 'budget' in kwargs and kwargs['budget']:
            budget_data = kwargs['budget']
            
            if not campaign.budget:
                campaign.budget = Budget()
            
            if 'amount' in budget_data:
                campaign.budget.amount = budget_data['amount']
            
            if 'currency' in budget_data:
                campaign.budget.currency = budget_data['currency']
            
            if 'type' in budget_data:
                campaign.budget.type = budget_data['type']
            
            if 'spent' in budget_data:
                campaign.budget.spent = budget_data['spent']
            
            campaign.budget.calculate_remaining()
        
        # Update schedule
        if 'schedule' in kwargs and kwargs['schedule']:
            schedule_data = kwargs['schedule']
            
            if not campaign.schedule:
                campaign.schedule = Schedule()
            
            if 'start_date' in schedule_data:
                campaign.schedule.start_date = datetime.fromisoformat(schedule_data['start_date'])
            
            if 'end_date' in schedule_data:
                if schedule_data['end_date']:
                    campaign.schedule.end_date = datetime.fromisoformat(schedule_data['end_date'])
                else:
                    campaign.schedule.end_date = None
            
            if 'time_zone' in schedule_data:
                campaign.schedule.time_zone = schedule_data['time_zone']
            
            if 'days_of_week' in schedule_data:
                campaign.schedule.days_of_week = schedule_data['days_of_week']
            
            if 'hours_of_day' in schedule_data:
                campaign.schedule.hours_of_day = schedule_data['hours_of_day']
        
        # Update targeting
        if 'targeting' in kwargs and kwargs['targeting']:
            targeting_data = kwargs['targeting']
            
            if not campaign.targeting:
                campaign.targeting = Targeting()
            
            for key, value in targeting_data.items():
                if hasattr(campaign.targeting, key):
                    setattr(campaign.targeting, key, value)
        
        # Update creatives
        if 'creatives' in kwargs and kwargs['creatives']:
            creatives_data = kwargs['creatives']
            
            # Process each creative
            for creative_data in creatives_data:
                if 'id' in creative_data:
                    # Update existing creative
                    for i, creative in enumerate(campaign.creatives):
                        if creative.id == creative_data['id']:
                            for key, value in creative_data.items():
                                if key != 'id' and hasattr(creative, key):
                                    setattr(creative, key, value)
                            
                            creative.updated_at = datetime.utcnow()
                            campaign.creatives[i] = creative
                            break
                else:
                    # Add new creative
                    creative = Creative(
                        id=str(uuid.uuid4()),
                        type=creative_data.get('type', 'image'),
                        name=creative_data.get('name', f"Creative {len(campaign.creatives) + 1}"),
                        primary_text=creative_data.get('primary_text', ''),
                        headline=creative_data.get('headline', ''),
                        description=creative_data.get('description', ''),
                        call_to_action=creative_data.get('call_to_action', ''),
                        media_urls=creative_data.get('media_urls', []),
                        thumbnail_url=creative_data.get('thumbnail_url', ''),
                        destination_url=creative_data.get('destination_url', ''),
                        tracking_url=creative_data.get('tracking_url', ''),
                        ai_generated=creative_data.get('ai_generated', False),
                        ai_prompt=creative_data.get('ai_prompt', '')
                    )
                    campaign.creatives.append(creative)
        
        # Remove creatives
        if 'remove_creatives' in kwargs and kwargs['remove_creatives']:
            creative_ids = kwargs['remove_creatives']
            campaign.creatives = [c for c in campaign.creatives if c.id not in creative_ids]
        
        # Update timestamp
        campaign.updated_at = datetime.utcnow()
        
        # Save campaign
        campaign.save()
        
        return campaign.to_dict()
    
    def delete_campaign(self, campaign_id: str, user_id: str) -> bool:
        """
        Delete campaign
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            
        Returns:
            bool: True if deleted, False otherwise
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return False
        
        # Delete campaign
        campaign.delete()
        
        return True
    
    def publish_campaign(self, campaign_id: str, user_id: str) -> Dict:
        """
        Publish campaign to platform
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            
        Returns:
            Dict: Result with platform ID and status
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return {'error': 'Campaign not found'}
        
        # Check if campaign is ready to publish
        if not campaign.budget:
            return {'error': 'Campaign budget is required'}
        
        if not campaign.schedule:
            return {'error': 'Campaign schedule is required'}
        
        if not campaign.targeting:
            return {'error': 'Campaign targeting is required'}
        
        if not campaign.creatives or len(campaign.creatives) == 0:
            return {'error': 'Campaign creatives are required'}
        
        # Get platform connector
        connector = self._get_platform_connector(campaign.platform)
        
        if not connector:
            return {'error': f'Platform {campaign.platform} is not supported'}
        
        # Publish campaign
        result = connector.publish_campaign(campaign)
        
        if 'error' in result:
            return result
        
        # Update campaign with platform ID
        campaign.platform_campaign_id = result.get('platform_id')
        campaign.status = 'active'
        campaign.updated_at = datetime.utcnow()
        campaign.save()
        
        return {
            'platform_id': result.get('platform_id'),
            'status': 'active'
        }
    
    def pause_campaign(self, campaign_id: str, user_id: str) -> bool:
        """
        Pause campaign
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            
        Returns:
            bool: True if paused, False otherwise
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return False
        
        # Check if campaign can be paused
        if campaign.status != 'active':
            return False
        
        # Get platform connector
        connector = self._get_platform_connector(campaign.platform)
        
        if not connector:
            return False
        
        # Pause campaign
        result = connector.pause_campaign(campaign.platform_campaign_id)
        
        if not result:
            return False
        
        # Update campaign status
        campaign.status = 'paused'
        campaign.updated_at = datetime.utcnow()
        campaign.save()
        
        return True
    
    def resume_campaign(self, campaign_id: str, user_id: str) -> bool:
        """
        Resume campaign
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            
        Returns:
            bool: True if resumed, False otherwise
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return False
        
        # Check if campaign can be resumed
        if campaign.status != 'paused':
            return False
        
        # Get platform connector
        connector = self._get_platform_connector(campaign.platform)
        
        if not connector:
            return False
        
        # Resume campaign
        result = connector.resume_campaign(campaign.platform_campaign_id)
        
        if not result:
            return False
        
        # Update campaign status
        campaign.status = 'active'
        campaign.updated_at = datetime.utcnow()
        campaign.save()
        
        return True
    
    def optimize_campaign(self, campaign_id: str, user_id: str, optimization_type: str = 'auto') -> Dict:
        """
        Optimize campaign using AI
        
        Args:
            campaign_id (str): Campaign ID
            user_id (str): User ID
            optimization_type (str, optional): Optimization type. Defaults to 'auto'.
            
        Returns:
            Dict: Optimization result
        """
        # Find campaign
        campaign = Campaign.objects(id=campaign_id, user=user_id).first()
        
        if not campaign:
            return {'error': 'Campaign not found'}
        
        # Check if campaign has performance data
        if not campaign.performance or not campaign.performance.impressions:
            return {'error': 'Campaign does not have enough performance data for optimization'}
        
        # Get optimization AI
        result = self.optimization_ai.optimize_campaign(campaign, optimization_type)
        
        if 'error' in result:
            return result
        
        # Update campaign optimization
        if not campaign.optimization:
            campaign.optimization = Optimization()
        
        campaign.optimization.status = 'completed'
        campaign.optimization.recommendations = result.get('recommendations', [])
        campaign.optimization.last_optimized = datetime.utcnow()
        
        # Set next optimization time (24 hours later)
        campaign.optimization.next_optimization = datetime.utcnow().replace(
            hour=datetime.utcnow().hour + 24
        )
        
        # Save campaign
        campaign.save()
        
        return {
            'recommendations': result.get('recommendations', [])
        }
    
    def generate_targeting(self, user_id: str, platform: str, objective: str, 
                          industry: Optional[str] = None, product_category: Optional[str] = None) -> Dict:
        """
        Generate targeting using AI
        
        Args:
            user_id (str): User ID
            platform (str): Platform
            objective (str): Campaign objective
            industry (Optional[str], optional): Industry. Defaults to None.
            product_category (Optional[str], optional): Product category. Defaults to None.
            
        Returns:
            Dict: Generated targeting
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Generate targeting
        targeting = self.targeting_ai.generate_targeting(
            platform=platform,
            objective=objective,
            industry=industry,
            product_category=product_category
        )
        
        return targeting
    
    def generate_creative(self, user_id: str, platform: str, objective: str, 
                         creative_type: str, product_info: Dict) -> Dict:
        """
        Generate creative using AI
        
        Args:
            user_id (str): User ID
            platform (str): Platform
            objective (str): Campaign objective
            creative_type (str): Creative type (image, video, carousel)
            product_info (Dict): Product information
            
        Returns:
            Dict: Generated creative
        """
        # Find user
        user = User.objects(id=user_id).first()
        
        if not user:
            return {'error': 'User not found'}
        
        # Generate creative
        creative = self.creative_ai.generate_creative(
            platform=platform,
            objective=objective,
            creative_type=creative_type,
            product_info=product_info
        )
        
        return creative
    
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
