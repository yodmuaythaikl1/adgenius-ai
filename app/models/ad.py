"""
AdGenius AI Backend - Advertisement Model
"""
from datetime import datetime
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField, ListField, DictField, BooleanField

class Ad(Document):
    """Advertisement model for storing ad information"""
    
    # Basic Information
    ad_id = StringField(required=True, unique=True, max_length=255)
    campaign_id = StringField(required=True)
    name = StringField(required=True, max_length=255)
    
    # Platform Information
    platform = StringField(required=True, choices=['facebook', 'instagram', 'tiktok', 'shopee'])
    platform_ad_id = StringField(max_length=255)
    
    # Creative Content
    creative_type = StringField(required=True, choices=['image', 'video', 'carousel', 'collection'])
    headline = StringField(max_length=500)
    body_text = StringField(max_length=2000)
    call_to_action = StringField(max_length=100)
    media_urls = ListField(StringField())
    
    # Targeting
    audience_targeting = DictField()
    
    # Performance Metrics
    impressions = IntField(default=0)
    clicks = IntField(default=0)
    conversions = IntField(default=0)
    spent = FloatField(default=0.0)
    ctr = FloatField(default=0.0)  # Click-through rate
    cpc = FloatField(default=0.0)  # Cost per click
    cpa = FloatField(default=0.0)  # Cost per acquisition
    roas = FloatField(default=0.0)  # Return on ad spend
    
    # Status
    status = StringField(
        required=True,
        choices=['draft', 'active', 'paused', 'completed', 'deleted'],
        default='draft'
    )
    
    # AI Generated
    is_ai_generated = BooleanField(default=False)
    ai_confidence_score = FloatField(min_value=0.0, max_value=1.0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    started_at = DateTimeField()
    ended_at = DateTimeField()
    
    meta = {
        'collection': 'ads',
        'indexes': [
            'campaign_id',
            'platform',
            'status',
            'created_at'
        ]
    }
    
    def save(self, *args, **kwargs):
        """Override save to update updated_at timestamp"""
        self.updated_at = datetime.utcnow()
        return super(Ad, self).save(*args, **kwargs)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'ad_id': self.ad_id,
            'campaign_id': self.campaign_id,
            'name': self.name,
            'platform': self.platform,
            'platform_ad_id': self.platform_ad_id,
            'creative_type': self.creative_type,
            'headline': self.headline,
            'body_text': self.body_text,
            'call_to_action': self.call_to_action,
            'media_urls': self.media_urls,
            'audience_targeting': self.audience_targeting,
            'performance': {
                'impressions': self.impressions,
                'clicks': self.clicks,
                'conversions': self.conversions,
                'spent': self.spent,
                'ctr': self.ctr,
                'cpc': self.cpc,
                'cpa': self.cpa,
                'roas': self.roas
            },
            'status': self.status,
            'is_ai_generated': self.is_ai_generated,
            'ai_confidence_score': self.ai_confidence_score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }
