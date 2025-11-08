"""
AdGenius AI Backend - Campaign Model
"""
from datetime import datetime
from typing import Dict, List, Optional

from mongoengine import (
    Document, StringField, DateTimeField, FloatField, 
    IntField, BooleanField, DictField, ListField, 
    ReferenceField, EmbeddedDocument, EmbeddedDocumentField, 
    EmbeddedDocumentListField
)

from app.models.user import User

class Targeting(EmbeddedDocument):
    """Targeting model"""
    age_min = IntField(min_value=13, max_value=65)
    age_max = IntField(min_value=13, max_value=65)
    genders = ListField(StringField())  # male, female, all
    locations = ListField(DictField())
    interests = ListField(DictField())
    behaviors = ListField(DictField())
    custom_audiences = ListField(DictField())
    excluded_audiences = ListField(DictField())
    device_platforms = ListField(StringField())  # mobile, desktop
    platforms = ListField(StringField())  # facebook, instagram, audience_network
    placements = ListField(StringField())
    optimization_goal = StringField()  # REACH, IMPRESSIONS, LINK_CLICKS, etc.
    ai_enhanced = BooleanField(default=False)
    ai_recommendations = ListField(DictField())

class Creative(EmbeddedDocument):
    """Creative model"""
    id = StringField(required=True)
    type = StringField(required=True)  # image, video, carousel, collection
    name = StringField(required=True)
    status = StringField(default='draft')  # draft, active, paused, archived
    primary_text = StringField()
    headline = StringField()
    description = StringField()
    call_to_action = StringField()
    media_urls = ListField(StringField())
    thumbnail_url = StringField()
    destination_url = StringField()
    tracking_url = StringField()
    platform_creative_id = StringField()
    performance = DictField()
    ai_generated = BooleanField(default=False)
    ai_prompt = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class Budget(EmbeddedDocument):
    """Budget model"""
    amount = FloatField(required=True)
    currency = StringField(required=True, default='THB')
    type = StringField(required=True)  # daily, lifetime
    spent = FloatField(default=0.0)
    remaining = FloatField()
    
    def calculate_remaining(self):
        """Calculate remaining budget"""
        self.remaining = self.amount - self.spent

class Schedule(EmbeddedDocument):
    """Schedule model"""
    start_date = DateTimeField(required=True)
    end_date = DateTimeField()
    time_zone = StringField(default='Asia/Bangkok')
    days_of_week = ListField(IntField(min_value=0, max_value=6))  # 0=Sunday, 6=Saturday
    hours_of_day = ListField(IntField(min_value=0, max_value=23))

class Performance(EmbeddedDocument):
    """Performance model"""
    impressions = IntField(default=0)
    clicks = IntField(default=0)
    conversions = IntField(default=0)
    spend = FloatField(default=0.0)
    ctr = FloatField()  # Click-through rate
    cpc = FloatField()  # Cost per click
    cpm = FloatField()  # Cost per 1000 impressions
    conversion_rate = FloatField()
    cost_per_conversion = FloatField()
    roas = FloatField()  # Return on ad spend
    last_updated = DateTimeField()
    
    def calculate_metrics(self):
        """Calculate performance metrics"""
        # Calculate CTR
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
        else:
            self.ctr = 0
        
        # Calculate CPC
        if self.clicks > 0:
            self.cpc = self.spend / self.clicks
        else:
            self.cpc = 0
        
        # Calculate CPM
        if self.impressions > 0:
            self.cpm = (self.spend / self.impressions) * 1000
        else:
            self.cpm = 0
        
        # Calculate conversion rate
        if self.clicks > 0:
            self.conversion_rate = (self.conversions / self.clicks) * 100
        else:
            self.conversion_rate = 0
        
        # Calculate cost per conversion
        if self.conversions > 0:
            self.cost_per_conversion = self.spend / self.conversions
        else:
            self.cost_per_conversion = 0
        
        # Update last updated timestamp
        self.last_updated = datetime.utcnow()

class Optimization(EmbeddedDocument):
    """Optimization model"""
    status = StringField(default='pending')  # pending, in_progress, completed
    recommendations = ListField(DictField())
    applied_recommendations = ListField(DictField())
    last_optimized = DateTimeField()
    next_optimization = DateTimeField()
    optimization_history = ListField(DictField())
    auto_optimization = BooleanField(default=False)

class Campaign(Document):
    """Campaign model"""
    user = ReferenceField(User, required=True)
    name = StringField(required=True)
    platform = StringField(required=True)  # facebook, instagram, tiktok, shopee
    platform_campaign_id = StringField()
    status = StringField(default='draft')  # draft, active, paused, completed, archived
    objective = StringField(required=True)  # awareness, consideration, conversion
    budget = EmbeddedDocumentField(Budget)
    schedule = EmbeddedDocumentField(Schedule)
    targeting = EmbeddedDocumentField(Targeting)
    creatives = EmbeddedDocumentListField(Creative)
    performance = EmbeddedDocumentField(Performance, default=Performance)
    optimization = EmbeddedDocumentField(Optimization, default=Optimization)
    notes = StringField()
    tags = ListField(StringField())
    industry = StringField()
    product_category = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'campaigns',
        'indexes': [
            'user',
            'platform',
            'status',
            'created_at'
        ]
    }
    
    def to_dict(self) -> Dict:
        """
        Convert campaign to dictionary
        
        Returns:
            Dict: Campaign dictionary
        """
        return {
            'id': str(self.id),
            'user_id': str(self.user.id),
            'name': self.name,
            'platform': self.platform,
            'platform_campaign_id': self.platform_campaign_id,
            'status': self.status,
            'objective': self.objective,
            'budget': self._get_budget_dict() if self.budget else None,
            'schedule': self._get_schedule_dict() if self.schedule else None,
            'targeting': self._get_targeting_dict() if self.targeting else None,
            'creatives': self._get_creatives_list(),
            'performance': self._get_performance_dict() if self.performance else None,
            'optimization': self._get_optimization_dict() if self.optimization else None,
            'notes': self.notes,
            'tags': self.tags,
            'industry': self.industry,
            'product_category': self.product_category,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def _get_budget_dict(self) -> Dict:
        """
        Get budget dictionary
        
        Returns:
            Dict: Budget dictionary
        """
        return {
            'amount': self.budget.amount,
            'currency': self.budget.currency,
            'type': self.budget.type,
            'spent': self.budget.spent,
            'remaining': self.budget.remaining
        }
    
    def _get_schedule_dict(self) -> Dict:
        """
        Get schedule dictionary
        
        Returns:
            Dict: Schedule dictionary
        """
        return {
            'start_date': self.schedule.start_date.isoformat(),
            'end_date': self.schedule.end_date.isoformat() if self.schedule.end_date else None,
            'time_zone': self.schedule.time_zone,
            'days_of_week': self.schedule.days_of_week,
            'hours_of_day': self.schedule.hours_of_day
        }
    
    def _get_targeting_dict(self) -> Dict:
        """
        Get targeting dictionary
        
        Returns:
            Dict: Targeting dictionary
        """
        return {
            'age_min': self.targeting.age_min,
            'age_max': self.targeting.age_max,
            'genders': self.targeting.genders,
            'locations': self.targeting.locations,
            'interests': self.targeting.interests,
            'behaviors': self.targeting.behaviors,
            'custom_audiences': self.targeting.custom_audiences,
            'excluded_audiences': self.targeting.excluded_audiences,
            'device_platforms': self.targeting.device_platforms,
            'platforms': self.targeting.platforms,
            'placements': self.targeting.placements,
            'optimization_goal': self.targeting.optimization_goal,
            'ai_enhanced': self.targeting.ai_enhanced,
            'ai_recommendations': self.targeting.ai_recommendations
        }
    
    def _get_creatives_list(self) -> List[Dict]:
        """
        Get creatives list
        
        Returns:
            List[Dict]: Creatives list
        """
        return [
            {
                'id': creative.id,
                'type': creative.type,
                'name': creative.name,
                'status': creative.status,
                'primary_text': creative.primary_text,
                'headline': creative.headline,
                'description': creative.description,
                'call_to_action': creative.call_to_action,
                'media_urls': creative.media_urls,
                'thumbnail_url': creative.thumbnail_url,
                'destination_url': creative.destination_url,
                'tracking_url': creative.tracking_url,
                'platform_creative_id': creative.platform_creative_id,
                'performance': creative.performance,
                'ai_generated': creative.ai_generated,
                'ai_prompt': creative.ai_prompt,
                'created_at': creative.created_at.isoformat(),
                'updated_at': creative.updated_at.isoformat()
            }
            for creative in self.creatives
        ]
    
    def _get_performance_dict(self) -> Dict:
        """
        Get performance dictionary
        
        Returns:
            Dict: Performance dictionary
        """
        return {
            'impressions': self.performance.impressions,
            'clicks': self.performance.clicks,
            'conversions': self.performance.conversions,
            'spend': self.performance.spend,
            'ctr': self.performance.ctr,
            'cpc': self.performance.cpc,
            'cpm': self.performance.cpm,
            'conversion_rate': self.performance.conversion_rate,
            'cost_per_conversion': self.performance.cost_per_conversion,
            'roas': self.performance.roas,
            'last_updated': self.performance.last_updated.isoformat() if self.performance.last_updated else None
        }
    
    def _get_optimization_dict(self) -> Dict:
        """
        Get optimization dictionary
        
        Returns:
            Dict: Optimization dictionary
        """
        return {
            'status': self.optimization.status,
            'recommendations': self.optimization.recommendations,
            'applied_recommendations': self.optimization.applied_recommendations,
            'last_optimized': self.optimization.last_optimized.isoformat() if self.optimization.last_optimized else None,
            'next_optimization': self.optimization.next_optimization.isoformat() if self.optimization.next_optimization else None,
            'optimization_history': self.optimization.optimization_history,
            'auto_optimization': self.optimization.auto_optimization
        }
