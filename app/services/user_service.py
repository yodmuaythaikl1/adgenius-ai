"""
AdGenius AI Backend - User Service
"""
from typing import Optional, Dict
from app.models.user import User

class UserService:
    """User service"""
    
    def __init__(self):
        """Initialize user service"""
        pass
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            return User.objects(id=user_id).first()
        except:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return User.objects(email=email).first()
        except:
            return None
    
    def update_user(self, user_id: str, user_data: Dict) -> Optional[User]:
        """Update user"""
        try:
            user = User.objects(id=user_id).first()
            if not user:
                return None
            
            for key, value in user_data.items():
                if hasattr(user, key) and key not in ['id', 'email', 'password']:
                    setattr(user, key, value)
            
            user.save()
            return user
        except:
            return None
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        try:
            user = User.objects(id=user_id).first()
            if user:
                user.delete()
                return True
            return False
        except:
            return False
