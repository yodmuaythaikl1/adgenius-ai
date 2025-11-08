"""
AdGenius AI Backend - Authentication Service
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Union

from flask_bcrypt import Bcrypt
from mongoengine.errors import NotUniqueError

from app.models.user import User, UserSettings, Notification

# Create bcrypt instance
bcrypt = Bcrypt()

class AuthService:
    """Authentication service"""
    
    def create_user(self, email: str, password: str, name: str, **kwargs) -> User:
        """
        Create a new user
        
        Args:
            email (str): User email
            password (str): User password
            name (str): User name
            **kwargs: Additional user attributes
            
        Returns:
            User: Created user
        """
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create user settings
        settings = UserSettings()
        
        # Create welcome notification
        notification = Notification(
            id=str(uuid.uuid4()),
            title="ยินดีต้อนรับสู่ AdGenius AI",
            message="ขอบคุณที่ลงทะเบียนใช้งาน AdGenius AI เราหวังว่าคุณจะได้รับประสบการณ์ที่ดีในการใช้งานแพลตฟอร์มของเรา",
            type="info"
        )
        
        # Create user
        user = User(
            email=email,
            password=hashed_password,
            name=name,
            settings=settings,
            notifications=[notification],
            last_login=datetime.utcnow(),
            **kwargs
        )
        
        try:
            user.save()
        except NotUniqueError:
            # Email already exists
            return None
        
        return user
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Authenticate user
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            Optional[User]: Authenticated user or None
        """
        # Find user by email
        user = User.objects(email=email).first()
        
        if not user:
            return None
        
        # Check password
        if not bcrypt.check_password_hash(user.password, password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        user.save()
        
        return user
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id (str): User ID
            
        Returns:
            Optional[User]: User or None
        """
        return User.objects(id=user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            Optional[User]: User or None
        """
        return User.objects(email=email).first()
    
    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id (str): User ID
            current_password (str): Current password
            new_password (str): New password
            
        Returns:
            bool: True if password changed, False otherwise
        """
        # Find user
        user = self.get_user_by_id(user_id)
        
        if not user:
            return False
        
        # Check current password
        if not bcrypt.check_password_hash(user.password, current_password):
            return False
        
        # Hash new password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        # Update password
        user.password = hashed_password
        user.updated_at = datetime.utcnow()
        user.save()
        
        # Add notification
        notification = Notification(
            id=str(uuid.uuid4()),
            title="รหัสผ่านถูกเปลี่ยนแปลง",
            message="รหัสผ่านของคุณได้ถูกเปลี่ยนแปลงเรียบร้อยแล้ว หากคุณไม่ได้ดำเนินการนี้ โปรดติดต่อฝ่ายสนับสนุนทันที",
            type="info"
        )
        
        user.notifications.append(notification)
        user.save()
        
        return True
    
    def reset_password(self, email: str) -> bool:
        """
        Reset user password
        
        Args:
            email (str): User email
            
        Returns:
            bool: True if password reset initiated, False otherwise
        """
        # Find user
        user = self.get_user_by_email(email)
        
        if not user:
            return False
        
        # In a real application, you would generate a reset token and send an email
        # For this example, we'll just add a notification
        
        notification = Notification(
            id=str(uuid.uuid4()),
            title="การรีเซ็ตรหัสผ่าน",
            message="คำขอรีเซ็ตรหัสผ่านได้ถูกส่งไปยังอีเมลของคุณแล้ว โปรดตรวจสอบอีเมลและทำตามคำแนะนำ",
            type="info"
        )
        
        user.notifications.append(notification)
        user.save()
        
        return True
