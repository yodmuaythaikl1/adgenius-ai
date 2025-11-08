"""
AdGenius AI Backend - Analytics Model
"""
from datetime import datetime
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, DictField, ListField

class CampaignAnalytics(Document):
    """Campaign analytics model for storing performance data"""
    
    # Reference Information
    campaign_id = StringField(required=True)
    user_id = StringField(required=True)
    
    # Time Period
    date = DateTimeField(required=True)
    period_type = StringField(
        required=True,
        choices=['hourly', 'daily', 'weekly', 'monthly'],
        default='daily'
    )
    
    # Performance Metrics
    impressions = IntField(default=0)
    clicks = IntField(default=0)
    conversions = IntField(default=0)
    spent = FloatField(default=0.0)
    revenue = FloatField(default=0.0)
    
    # Calculated Metrics
    ctr = FloatField(default=0.0)  # Click-through rate
    cpc = FloatField(default=0.0)  # Cost per click
    cpm = FloatField(default=0.0)  # Cost per mille (thousand impressions)
    cpa = FloatField(default=0.0)  # Cost per acquisition
    roas = FloatField(default=0.0)  # Return on ad spend
    conversion_rate = FloatField(default=0.0)
    
    # Platform Breakdown
    platform_metrics = DictField()  # Metrics per platform
    
    # Audience Insights
    demographic_data = DictField()  # Age, gender, location breakdown
    device_data = DictField()  # Desktop, mobile, tablet
    
    # Top Performing Elements
    top_ads = ListField(DictField())  # Best performing ads
    top_keywords = ListField(DictField())  # Best performing keywords
    
    # AI Insights
    ai_recommendations = ListField(StringField())
    optimization_score = FloatField(min_value=0.0, max_value=100.0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'campaign_analytics',
        'indexes': [
            'campaign_id',
            'user_id',
            'date',
            ('campaign_id', 'date')
        ]
    }
    
    def save(self, *args, **kwargs):
        """Override save to update calculated metrics and timestamp"""
        self.updated_at = datetime.utcnow()
        
        # Calculate metrics
        if self.impressions > 0:
            self.ctr = (self.clicks / self.impressions) * 100
            self.cpm = (self.spent / self.impressions) * 1000
        
        if self.clicks > 0:
            self.cpc = self.spent / self.clicks
            self.conversion_rate = (self.conversions / self.clicks) * 100
        
        if self.conversions > 0:
            self.cpa = self.spent / self.conversions
        
        if self.spent > 0:
            self.roas = self.revenue / self.spent
        
        return super(CampaignAnalytics, self).save(*args, **kwargs)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'campaign_id': self.campaign_id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'period_type': self.period_type,
            'metrics': {
                'impressions': self.impressions,
                'clicks': self.clicks,
                'conversions': self.conversions,
                'spent': self.spent,
                'revenue': self.revenue,
                'ctr': round(self.ctr, 2),
                'cpc': round(self.cpc, 2),
                'cpm': round(self.cpm, 2),
                'cpa': round(self.cpa, 2),
                'roas': round(self.roas, 2),
                'conversion_rate': round(self.conversion_rate, 2)
            },
            'platform_metrics': self.platform_metrics,
            'demographic_data': self.demographic_data,
            'device_data': self.device_data,
            'top_ads': self.top_ads,
            'top_keywords': self.top_keywords,
            'ai_insights': {
                'recommendations': self.ai_recommendations,
                'optimization_score': self.optimization_score
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
