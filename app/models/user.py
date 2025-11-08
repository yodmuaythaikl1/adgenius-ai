"""
AdGenius AI Backend - User Model
"""
from datetime import datetime
from typing import Dict, List, Optional

from mongoengine import (
    Document, StringField, EmailField, DateTimeField, 
    BooleanField, DictField, ListField, ReferenceField, 
    EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField
)

class PlatformAccount(EmbeddedDocument):
    """Platform account model"""
    platform = StringField(required=True)  # facebook, instagram, tiktok, shopee
    account_id = StringField(required=True)
    account_name = StringField(required=True)
    access_token = StringField()
    refresh_token = StringField()
    token_expires_at = DateTimeField()
    status = StringField(default='active')  # active, inactive, expired
    meta_data = DictField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

class Notification(EmbeddedDocument):
    """Notification model"""
    id = StringField(required=True)
    title = StringField(required=True)
    message = StringField(required=True)
    type = StringField(required=True)  # info, warning, error, success
    read = BooleanField(default=False)
    data = DictField()
    created_at = DateTimeField(default=datetime.utcnow)

class UserSettings(EmbeddedDocument):
    """User settings model"""
    email_notifications = BooleanField(default=True)
    campaign_alerts = BooleanField(default=True)
    performance_reports = BooleanField(default=True)
    report_frequency = StringField(default='weekly')  # daily, weekly, monthly
    timezone = StringField(default='UTC')
    language = StringField(default='en')
    theme = StringField(default='light')  # light, dark
    dashboard_widgets = ListField(StringField())

class User(Document):
    """User model"""
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True)
    company = StringField()
    phone = StringField()
    role = StringField(default='user')  # user, admin
    status = StringField(default='active')  # active, inactive, suspended
    profile_image = StringField()
    platform_accounts = EmbeddedDocumentListField(PlatformAccount)
    settings = EmbeddedDocumentField(UserSettings, default=UserSettings)
    notifications = EmbeddedDocumentListField(Notification)
    last_login = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'status'
        ]
    }
    
    def to_dict(self) -> Dict:
        """
        Convert user to dictionary
        
        Returns:
            Dict: User dictionary
        """
        return {
            'id': str(self.id),
            'email': self.email,
            'name': self.name,
            'company': self.company,
            'phone': self.phone,
            'role': self.role,
            'status': self.status,
            'profile_image': self.profile_image,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def get_platform_accounts(self) -> List[Dict]:
        """
        Get platform accounts
        
        Returns:
            List[Dict]: Platform accounts
        """
        return [
            {
                'platform': account.platform,
                'account_id': account.account_id,
                'account_name': account.account_name,
                'status': account.status,
                'created_at': account.created_at.isoformat(),
                'updated_at': account.updated_at.isoformat()
            }
            for account in self.platform_accounts
        ]
    
    def get_settings(self) -> Dict:
        """
        Get user settings
        
        Returns:
            Dict: User settings
        """
        if not self.settings:
            return {}
        
        return {
            'email_notifications': self.settings.email_notifications,
            'campaign_alerts': self.settings.campaign_alerts,
            'performance_reports': self.settings.performance_reports,
            'report_frequency': self.settings.report_frequency,
            'timezone': self.settings.timezone,
            'language': self.settings.language,
            'theme': self.settings.theme,
            'dashboard_widgets': self.settings.dashboard_widgets
        }
    
    def get_notifications(self, read: Optional[bool] = None) -> List[Dict]:
        """
        Get notifications
        
        Args:
            read (Optional[bool], optional): Filter by read status. Defaults to None.
            
        Returns:
            List[Dict]: Notifications
        """
        notifications = self.notifications
        
        if read is not None:
            notifications = [n for n in notifications if n.read == read]
        
        return [
            {
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.type,
                'read': notification.read,
                'data': notification.data,
                'created_at': notification.created_at.isoformat()
            }
            for notification in notifications
        ]
