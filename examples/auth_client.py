"""Example authentication client for AI Adoption Dashboard API.

This script demonstrates how to authenticate with the API and use protected endpoints.
"""

import requests
import json
from typing import Optional, Dict, Any
import time


class AuthClient:
    """Client for authenticated API access."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize auth client."""
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[float] = None
        
    def login(self, username: str, password: str) -> bool:
        """Login to the API."""
        url = f"{self.base_url}/api/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                self.access_token = result["data"]["access_token"]
                self.refresh_token = result["data"]["refresh_token"]
                # Assume token expires in 30 minutes
                self.token_expiry = time.time() + (30 * 60)
                print(f"✅ Logged in as {username}")
                return True
            else:
                print(f"❌ Login failed: {response.json()['message']}")
                return False
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    def register(self, username: str, email: str, password: str, role: str = "viewer") -> bool:
        """Register a new user."""
        url = f"{self.base_url}/api/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"✅ User {username} registered successfully")
                return True
            else:
                print(f"❌ Registration failed: {response.json()['message']}")
                return False
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    def refresh_access_token(self) -> bool:
        """Refresh the access token."""
        if not self.refresh_token:
            print("❌ No refresh token available")
            return False
            
        url = f"{self.base_url}/api/auth/refresh"
        data = {"refresh_token": self.refresh_token}
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                self.access_token = result["data"]["access_token"]
                self.refresh_token = result["data"]["refresh_token"]
                self.token_expiry = time.time() + (30 * 60)
                print("✅ Token refreshed successfully")
                return True
            else:
                print(f"❌ Token refresh failed: {response.json()['message']}")
                return False
        except Exception as e:
            print(f"❌ Token refresh error: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers."""
        if not self.access_token:
            raise ValueError("Not authenticated. Please login first.")
            
        # Check if token might be expired
        if self.token_expiry and time.time() > self.token_expiry:
            print("⚠️  Token might be expired, attempting refresh...")
            if not self.refresh_access_token():
                raise ValueError("Failed to refresh token")
                
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_profile(self) -> Optional[Dict[str, Any]]:
        """Get user profile."""
        url = f"{self.base_url}/api/auth/profile"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()["data"]["profile"]
            else:
                print(f"❌ Failed to get profile: {response.json()['message']}")
                return None
        except Exception as e:
            print(f"❌ Profile error: {e}")
            return None
    
    def get_permissions(self) -> Optional[List[str]]:
        """Get user permissions."""
        url = f"{self.base_url}/api/auth/permissions"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()["data"]["permissions"]
            else:
                print(f"❌ Failed to get permissions: {response.json()['message']}")
                return None
        except Exception as e:
            print(f"❌ Permissions error: {e}")
            return None
    
    def calculate_npv(self, cash_flows: List[float], discount_rate: float, initial_investment: float) -> Optional[float]:
        """Calculate NPV (protected endpoint)."""
        url = f"{self.base_url}/api/financial/npv"
        data = {
            "cash_flows": cash_flows,
            "discount_rate": discount_rate,
            "initial_investment": initial_investment
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()["data"]["npv"]
            else:
                print(f"❌ NPV calculation failed: {response.json()['message']}")
                return None
        except Exception as e:
            print(f"❌ NPV error: {e}")
            return None
    
    def generate_api_key(self, key_name: str, permissions: List[str]) -> Optional[str]:
        """Generate API key for programmatic access."""
        url = f"{self.base_url}/api/auth/generate-api-key"
        data = {
            "key_name": key_name,
            "permissions": permissions
        }
        
        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()["data"]["api_key"]
            else:
                print(f"❌ API key generation failed: {response.json()['message']}")
                return None
        except Exception as e:
            print(f"❌ API key error: {e}")
            return None
    
    def list_users(self) -> Optional[List[Dict[str, Any]]]:
        """List all users (admin only)."""
        url = f"{self.base_url}/api/auth/users"
        
        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()["data"]["users"]
            else:
                print(f"❌ Failed to list users: {response.json()['message']}")
                return None
        except Exception as e:
            print(f"❌ List users error: {e}")
            return None


def main():
    """Demonstrate authentication functionality."""
    client = AuthClient()
    
    print("=== AI Adoption Dashboard Auth Demo ===\n")
    
    # Try to login with default admin account
    print("1. Logging in as admin...")
    if client.login("admin", "admin123"):
        
        # Get profile
        print("\n2. Getting user profile...")
        profile = client.get_profile()
        if profile:
            print(f"   Username: {profile['username']}")
            print(f"   Email: {profile['email']}")
            print(f"   Role: {profile['role']}")
            print(f"   Created: {profile['created_at']}")
        
        # Get permissions
        print("\n3. Getting permissions...")
        permissions = client.get_permissions()
        if permissions:
            print(f"   Permissions: {', '.join(permissions[:5])}...")
        
        # Try a protected calculation
        print("\n4. Testing protected NPV calculation...")
        npv = client.calculate_npv(
            cash_flows=[100000, 120000, 140000],
            discount_rate=0.10,
            initial_investment=300000
        )
        if npv:
            print(f"   NPV: ${npv:,.2f}")
        
        # Create a new user (admin only)
        print("\n5. Creating new analyst user...")
        if client.register("analyst1", "analyst@example.com", "analyst123", "analyst"):
            
            # List users (admin only)
            print("\n6. Listing all users...")
            users = client.list_users()
            if users:
                for user in users:
                    print(f"   - {user['username']} ({user['role']})")
        
        # Generate API key
        print("\n7. Generating API key...")
        api_key = client.generate_api_key(
            "Demo API Key",
            ["read:calculations", "read:exports"]
        )
        if api_key:
            print(f"   API Key: {api_key[:20]}... (store securely!)")
    
    # Try to login as the new analyst
    print("\n8. Logging in as analyst...")
    if client.login("analyst1", "analyst123"):
        profile = client.get_profile()
        if profile:
            print(f"   Logged in as: {profile['username']} ({profile['role']})")
        
        # Try admin-only operation (should fail)
        print("\n9. Trying admin operation as analyst (should fail)...")
        users = client.list_users()
        if not users:
            print("   ✅ Correctly denied admin access")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()