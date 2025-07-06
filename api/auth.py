"""Authentication and authorization module for AI Adoption Dashboard.

This module provides JWT-based authentication, user management,
and role-based access control.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User roles
class UserRole:
    """User role definitions."""
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    API_USER = "api_user"

# Role permissions
ROLE_PERMISSIONS = {
    UserRole.ADMIN: [
        "read:all",
        "write:all",
        "delete:all",
        "admin:users",
        "admin:settings"
    ],
    UserRole.ANALYST: [
        "read:calculations",
        "write:calculations",
        "read:reports",
        "write:reports",
        "read:exports",
        "write:exports"
    ],
    UserRole.VIEWER: [
        "read:calculations",
        "read:reports",
        "read:exports"
    ],
    UserRole.API_USER: [
        "read:calculations",
        "write:calculations",
        "read:exports"
    ]
}


# Pydantic models
class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: str = Field(default=UserRole.VIEWER)
    is_active: bool = True


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)


class UserInDB(UserBase):
    """User model with hashed password."""
    hashed_password: str
    created_at: datetime
    last_login: Optional[datetime] = None


class User(UserBase):
    """User response model."""
    id: str
    created_at: datetime
    last_login: Optional[datetime] = None


class Token(BaseModel):
    """Token response model."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None
    scopes: List[str] = []


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class PasswordReset(BaseModel):
    """Password reset model."""
    old_password: str
    new_password: str = Field(..., min_length=8)


class UserDatabase:
    """Simple file-based user database."""
    
    def __init__(self, db_path: str = "users.json"):
        """Initialize user database."""
        self.db_path = Path(db_path)
        self.users: Dict[str, Dict[str, Any]] = {}
        self._load_users()
        
        # Create default admin user if no users exist
        if not self.users:
            self._create_default_admin()
    
    def _load_users(self):
        """Load users from file."""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r') as f:
                    self.users = json.load(f)
            except Exception as e:
                logger.error(f"Error loading users: {e}")
                self.users = {}
    
    def _save_users(self):
        """Save users to file."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.users, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving users: {e}")
    
    def _create_default_admin(self):
        """Create default admin user."""
        admin_user = {
            "username": "admin",
            "email": "admin@example.com",
            "full_name": "Administrator",
            "role": UserRole.ADMIN,
            "is_active": True,
            "hashed_password": get_password_hash("admin123"),
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None
        }
        self.users["admin"] = admin_user
        self._save_users()
        logger.info("Default admin user created (username: admin, password: admin123)")
    
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username."""
        return self.users.get(username)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user."""
        username = user_data["username"]
        if username in self.users:
            raise ValueError(f"User {username} already exists")
        
        self.users[username] = user_data
        self._save_users()
        return user_data
    
    def update_user(self, username: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update user data."""
        if username not in self.users:
            return None
        
        self.users[username].update(updates)
        self._save_users()
        return self.users[username]
    
    def delete_user(self, username: str) -> bool:
        """Delete user."""
        if username in self.users:
            del self.users[username]
            self._save_users()
            return True
        return False
    
    def list_users(self) -> List[Dict[str, Any]]:
        """List all users."""
        return list(self.users.values())


# Initialize user database
user_db = UserDatabase()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user with username and password."""
    user = user_db.get_user(username)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    
    # Update last login
    user_db.update_user(username, {"last_login": datetime.utcnow().isoformat()})
    return user


def create_user(user_create: UserCreate) -> User:
    """Create new user account."""
    # Check if user exists
    if user_db.get_user(user_create.username):
        raise ValueError(f"Username {user_create.username} already registered")
    
    # Create user
    user_data = {
        "username": user_create.username,
        "email": user_create.email,
        "full_name": user_create.full_name,
        "role": user_create.role,
        "is_active": user_create.is_active,
        "hashed_password": get_password_hash(user_create.password),
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None
    }
    
    created_user = user_db.create_user(user_data)
    
    # Return user without password
    return User(
        id=created_user["username"],
        username=created_user["username"],
        email=created_user["email"],
        full_name=created_user["full_name"],
        role=created_user["role"],
        is_active=created_user["is_active"],
        created_at=created_user["created_at"],
        last_login=created_user["last_login"]
    )


def get_current_user_permissions(username: str) -> List[str]:
    """Get permissions for user based on role."""
    user = user_db.get_user(username)
    if not user:
        return []
    
    role = user.get("role", UserRole.VIEWER)
    return ROLE_PERMISSIONS.get(role, [])


def check_permission(username: str, permission: str) -> bool:
    """Check if user has specific permission."""
    permissions = get_current_user_permissions(username)
    
    # Check exact match
    if permission in permissions:
        return True
    
    # Check wildcard permissions (e.g., "read:all" covers "read:calculations")
    permission_parts = permission.split(":")
    if len(permission_parts) == 2:
        action, resource = permission_parts
        if f"{action}:all" in permissions:
            return True
    
    return False


def update_password(username: str, old_password: str, new_password: str) -> bool:
    """Update user password."""
    user = user_db.get_user(username)
    if not user:
        return False
    
    if not verify_password(old_password, user["hashed_password"]):
        return False
    
    user_db.update_user(username, {
        "hashed_password": get_password_hash(new_password)
    })
    
    return True


def generate_api_key(username: str, key_name: str, permissions: List[str]) -> str:
    """Generate API key for programmatic access."""
    # Create a non-expiring token with limited permissions
    data = {
        "sub": username,
        "type": "api_key",
        "key_name": key_name,
        "permissions": permissions
    }
    
    # API keys don't expire
    api_key = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    # Store API key reference in user data
    user = user_db.get_user(username)
    if user:
        api_keys = user.get("api_keys", [])
        api_keys.append({
            "key_name": key_name,
            "key_prefix": api_key[:20] + "...",
            "permissions": permissions,
            "created_at": datetime.utcnow().isoformat()
        })
        user_db.update_user(username, {"api_keys": api_keys})
    
    return api_key


class AuthManager:
    """Authentication manager for API endpoints."""
    
    @staticmethod
    def login(username: str, password: str) -> Token:
        """Authenticate user and return tokens."""
        user = authenticate_user(username, password)
        if not user:
            raise ValueError("Invalid username or password")
        
        if not user.get("is_active", True):
            raise ValueError("User account is inactive")
        
        # Create tokens
        access_token_data = {
            "sub": user["username"],
            "role": user["role"],
            "scopes": get_current_user_permissions(user["username"])
        }
        
        access_token = create_access_token(access_token_data)
        refresh_token = create_refresh_token({"sub": user["username"]})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Token:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid refresh token")
        
        username = payload.get("sub")
        user = user_db.get_user(username)
        if not user or not user.get("is_active", True):
            raise ValueError("User not found or inactive")
        
        # Create new tokens
        access_token_data = {
            "sub": user["username"],
            "role": user["role"],
            "scopes": get_current_user_permissions(user["username"])
        }
        
        new_access_token = create_access_token(access_token_data)
        new_refresh_token = create_refresh_token({"sub": user["username"]})
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )
    
    @staticmethod
    def validate_token(token: str) -> Optional[TokenData]:
        """Validate access token and return token data."""
        payload = decode_token(token)
        if not payload:
            return None
        
        username = payload.get("sub")
        if not username:
            return None
        
        return TokenData(
            username=username,
            scopes=payload.get("scopes", [])
        )


# Initialize auth manager
auth_manager = AuthManager()