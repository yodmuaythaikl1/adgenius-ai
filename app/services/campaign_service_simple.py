"""
AdGenius AI Backend - Campaign Service (Simplified)
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from app.models.campaign import Campaign

class CampaignService:
    """Simplified Campaign service without AI dependencies"""
    
    def __init__(self):
        """Initialize campaign service"""
        pass
    
    def get_campaigns(self, user_id: str, page: int = 1, per_page: int = 10, 
                     platform: Optional[str] = None, status: Optional[str] = None) -> Dict:
        """Get campaigns for user"""
        try:
            campaigns = Campaign.objects(user_id=user_id)
            
            if platform:
                campaigns = campaigns.filter(platform=platform)
            if status:
                campaigns = campaigns.filter(status=status)
            
            total = campaigns.count()
            campaigns = campaigns.skip((page - 1) * per_page).limit(per_page)
            
            return {
                "campaigns": [c.to_dict() for c in campaigns],
                "total": total,
                "page": page,
                "per_page": per_page
            }
        except Exception as e:
            return {"campaigns": [], "total": 0, "page": page, "per_page": per_page, "error": str(e)}
    
    def get_campaign(self, campaign_id: str, user_id: str) -> Optional[Campaign]:
        """Get single campaign"""
        try:
            return Campaign.objects(id=campaign_id, user_id=user_id).first()
        except:
            return None
    
    def create_campaign(self, user_id: str, campaign_data: Dict) -> Optional[Campaign]:
        """Create new campaign"""
        try:
            campaign = Campaign(
                user_id=user_id,
                name=campaign_data.get('name', 'Untitled Campaign'),
                platform=campaign_data.get('platform', 'facebook'),
                objective=campaign_data.get('objective', 'awareness'),
                status='draft',
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            campaign.save()
            return campaign
        except Exception as e:
            print(f"Error creating campaign: {e}")
            return None
    
    def update_campaign(self, campaign_id: str, user_id: str, campaign_data: Dict) -> Optional[Campaign]:
        """Update campaign"""
        try:
            campaign = Campaign.objects(id=campaign_id, user_id=user_id).first()
            if not campaign:
                return None
            
            for key, value in campaign_data.items():
                if hasattr(campaign, key):
                    setattr(campaign, key, value)
            
            campaign.updated_at = datetime.utcnow()
            campaign.save()
            return campaign
        except:
            return None
    
    def delete_campaign(self, campaign_id: str, user_id: str) -> bool:
        """Delete campaign"""
        try:
            campaign = Campaign.objects(id=campaign_id, user_id=user_id).first()
            if campaign:
                campaign.delete()
                return True
            return False
        except:
            return False
