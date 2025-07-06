"""Authentication API endpoints for AI Adoption Dashboard.

This module provides API endpoints for user authentication,
registration, and access control.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth import (
    auth_manager,
    user_db,
    create_user,
    UserCreate,
    User,
    Token,
    LoginRequest,
    PasswordReset,
    TokenData,
    check_permission,
    update_password,
    generate_api_key,
    UserRole
)
from .endpoints import APIResponse, log_api_call
from utils.audit_logger import audit_logger

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    token_data = auth_manager.validate_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data


def require_permission(permission: str):
    """Decorator to require specific permission for endpoint access."""
    def permission_checker(current_user: TokenData = Depends(get_current_user)):
        has_permission = check_permission(current_user.username, permission)
        
        # Audit permission check
        audit_logger.log_permission_check(
            user=current_user.username,
            permission=permission,
            granted=has_permission
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required: {permission}"
            )
        return current_user
    return permission_checker


class AuthAPI:
    """Authentication API endpoints."""
    
    @staticmethod
    @log_api_call("auth/login")
    def login(request_data: LoginRequest) -> Dict:
        """User login endpoint.
        
        Returns access and refresh tokens.
        """
        try:
            token = auth_manager.login(request_data.username, request_data.password)
            
            # Audit successful login
            audit_logger.log_authentication(
                action="login",
                username=request_data.username,
                success=True,
                details={"method": "password"}
            )
            
            return APIResponse.success({
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "token_type": token.token_type,
                "user": {
                    "username": request_data.username,
                    "role": user_db.get_user(request_data.username).get("role")
                }
            }, "Login successful")
            
        except ValueError as e:
            # Audit failed login
            audit_logger.log_authentication(
                action="login",
                username=request_data.username,
                success=False,
                details={"reason": str(e)}
            )
            return APIResponse.error(str(e), 401)
        except Exception as e:
            logger.error(f"Login error: {e}")
            audit_logger.log_authentication(
                action="login",
                username=request_data.username,
                success=False,
                details={"error": str(e)}
            )
            return APIResponse.error("Login failed", 500)
    
    @staticmethod
    @log_api_call("auth/register")
    def register(request_data: UserCreate) -> Dict:
        """User registration endpoint.
        
        Creates new user account.
        """
        try:
            # Only admins can create users with admin role
            if request_data.role == UserRole.ADMIN:
                return APIResponse.error("Cannot self-register as admin", 403)
            
            user = create_user(request_data)
            
            return APIResponse.success({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }, "User created successfully")
            
        except ValueError as e:
            return APIResponse.error(str(e), 400)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return APIResponse.error("Registration failed", 500)
    
    @staticmethod
    @log_api_call("auth/refresh")
    def refresh_token(request_data: Dict) -> Dict:
        """Refresh access token using refresh token."""
        try:
            refresh_token = request_data.get("refresh_token")
            if not refresh_token:
                return APIResponse.error("Refresh token required", 400)
            
            token = auth_manager.refresh_token(refresh_token)
            
            return APIResponse.success({
                "access_token": token.access_token,
                "refresh_token": token.refresh_token,
                "token_type": token.token_type
            }, "Token refreshed successfully")
            
        except ValueError as e:
            return APIResponse.error(str(e), 401)
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return APIResponse.error("Token refresh failed", 500)
    
    @staticmethod
    @log_api_call("auth/profile")
    def get_profile(username: str) -> Dict:
        """Get user profile information."""
        try:
            user = user_db.get_user(username)
            if not user:
                return APIResponse.error("User not found", 404)
            
            # Remove sensitive information
            profile = {
                "username": user["username"],
                "email": user["email"],
                "full_name": user.get("full_name"),
                "role": user["role"],
                "is_active": user["is_active"],
                "created_at": user["created_at"],
                "last_login": user.get("last_login")
            }
            
            return APIResponse.success({"profile": profile})
            
        except Exception as e:
            logger.error(f"Profile retrieval error: {e}")
            return APIResponse.error("Failed to get profile", 500)
    
    @staticmethod
    @log_api_call("auth/change-password")
    def change_password(username: str, request_data: PasswordReset) -> Dict:
        """Change user password."""
        try:
            success = update_password(
                username,
                request_data.old_password,
                request_data.new_password
            )
            
            if success:
                return APIResponse.success({}, "Password changed successfully")
            else:
                return APIResponse.error("Invalid old password", 400)
                
        except Exception as e:
            logger.error(f"Password change error: {e}")
            return APIResponse.error("Failed to change password", 500)
    
    @staticmethod
    @log_api_call("auth/users")
    def list_users() -> Dict:
        """List all users (admin only)."""
        try:
            users = user_db.list_users()
            
            # Remove sensitive information
            safe_users = []
            for user in users:
                safe_users.append({
                    "username": user["username"],
                    "email": user["email"],
                    "full_name": user.get("full_name"),
                    "role": user["role"],
                    "is_active": user["is_active"],
                    "created_at": user["created_at"],
                    "last_login": user.get("last_login")
                })
            
            return APIResponse.success({"users": safe_users})
            
        except Exception as e:
            logger.error(f"User list error: {e}")
            return APIResponse.error("Failed to list users", 500)
    
    @staticmethod
    @log_api_call("auth/create-user")
    def create_user_admin(request_data: UserCreate) -> Dict:
        """Create new user (admin only)."""
        try:
            user = create_user(request_data)
            
            return APIResponse.success({
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role
                }
            }, "User created successfully")
            
        except ValueError as e:
            return APIResponse.error(str(e), 400)
        except Exception as e:
            logger.error(f"User creation error: {e}")
            return APIResponse.error("Failed to create user", 500)
    
    @staticmethod
    @log_api_call("auth/update-user")
    def update_user(username: str, request_data: Dict) -> Dict:
        """Update user information (admin only)."""
        try:
            allowed_updates = ["email", "full_name", "role", "is_active"]
            updates = {k: v for k, v in request_data.items() if k in allowed_updates}
            
            updated_user = user_db.update_user(username, updates)
            
            if updated_user:
                return APIResponse.success({
                    "user": {
                        "username": updated_user["username"],
                        "email": updated_user["email"],
                        "full_name": updated_user.get("full_name"),
                        "role": updated_user["role"],
                        "is_active": updated_user["is_active"]
                    }
                }, "User updated successfully")
            else:
                return APIResponse.error("User not found", 404)
                
        except Exception as e:
            logger.error(f"User update error: {e}")
            return APIResponse.error("Failed to update user", 500)
    
    @staticmethod
    @log_api_call("auth/delete-user")
    def delete_user(username: str) -> Dict:
        """Delete user (admin only)."""
        try:
            success = user_db.delete_user(username)
            
            if success:
                return APIResponse.success({}, "User deleted successfully")
            else:
                return APIResponse.error("User not found", 404)
                
        except Exception as e:
            logger.error(f"User deletion error: {e}")
            return APIResponse.error("Failed to delete user", 500)
    
    @staticmethod
    @log_api_call("auth/generate-api-key")
    def create_api_key(username: str, request_data: Dict) -> Dict:
        """Generate API key for user."""
        try:
            key_name = request_data.get("key_name", f"API Key {datetime.now().strftime('%Y%m%d%H%M%S')}")
            permissions = request_data.get("permissions", ["read:calculations", "read:exports"])
            
            # Validate permissions
            user = user_db.get_user(username)
            if not user:
                return APIResponse.error("User not found", 404)
            
            user_permissions = get_current_user_permissions(username)
            for perm in permissions:
                if perm not in user_permissions:
                    return APIResponse.error(f"Cannot grant permission: {perm}", 403)
            
            api_key = generate_api_key(username, key_name, permissions)
            
            return APIResponse.success({
                "api_key": api_key,
                "key_name": key_name,
                "permissions": permissions,
                "note": "Store this key securely. It cannot be retrieved again."
            }, "API key generated successfully")
            
        except Exception as e:
            logger.error(f"API key generation error: {e}")
            return APIResponse.error("Failed to generate API key", 500)
    
    @staticmethod
    @log_api_call("auth/permissions")
    def get_permissions(username: str) -> Dict:
        """Get user permissions."""
        try:
            from .auth import get_current_user_permissions
            
            permissions = get_current_user_permissions(username)
            
            return APIResponse.success({
                "username": username,
                "permissions": permissions
            })
            
        except Exception as e:
            logger.error(f"Permission retrieval error: {e}")
            return APIResponse.error("Failed to get permissions", 500)


# Initialize auth API instance
auth_api = AuthAPI()


# Protected endpoint example
def protected_endpoint_example(
    current_user: TokenData = Depends(get_current_user)
) -> Dict:
    """Example of a protected endpoint that requires authentication."""
    return APIResponse.success({
        "message": "This is a protected endpoint",
        "user": current_user.username,
        "scopes": current_user.scopes
    })


# Permission-based endpoint example
def admin_only_endpoint(
    current_user: TokenData = Depends(require_permission("admin:users"))
) -> Dict:
    """Example of an admin-only endpoint."""
    return APIResponse.success({
        "message": "This is an admin-only endpoint",
        "user": current_user.username
    })