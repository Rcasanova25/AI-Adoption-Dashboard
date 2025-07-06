# Authentication & Authorization Documentation

## Overview

The AI Adoption Dashboard API uses JWT (JSON Web Token) based authentication to secure endpoints and provide role-based access control (RBAC). This ensures that sensitive financial calculations and data are protected.

## Key Features

- **JWT-based Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Fine-grained permissions based on user roles
- **API Key Support**: Generate long-lived API keys for programmatic access
- **Token Refresh**: Automatic token refresh mechanism
- **User Management**: Complete user lifecycle management

## Default Credentials

On first launch, a default admin account is created:
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password immediately in production!

## User Roles

### 1. Admin
Full system access including:
- All calculations and reports
- User management
- System configuration
- API key generation for any permission

### 2. Analyst
Standard user with:
- Read/write access to calculations
- Read/write access to reports
- Export functionality
- API key generation (limited to own permissions)

### 3. Viewer
Read-only access to:
- Calculations
- Reports
- Exports

### 4. API User
Programmatic access with:
- Read/write calculations
- Read exports
- Optimized for automated systems

## Authentication Flow

### 1. Login
```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "status": "success",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "token_type": "bearer",
        "user": {
            "username": "your_username",
            "role": "analyst"
        }
    }
}
```

### 2. Using Protected Endpoints
Include the access token in the Authorization header:
```http
GET /api/financial/npv
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 3. Token Refresh
When the access token expires (30 minutes), use the refresh token:
```http
POST /api/auth/refresh
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## API Endpoints

### Authentication Endpoints

#### Login
`POST /api/auth/login`
- Public endpoint
- Returns access and refresh tokens

#### Register
`POST /api/auth/register`
- Public endpoint (limited roles)
- Cannot self-register as admin

#### Refresh Token
`POST /api/auth/refresh`
- Public endpoint
- Requires valid refresh token

#### Get Profile
`GET /api/auth/profile`
- Requires authentication
- Returns current user profile

#### Change Password
`POST /api/auth/change-password`
- Requires authentication
- Changes own password

#### Get Permissions
`GET /api/auth/permissions`
- Requires authentication
- Lists user's permissions

### User Management (Admin Only)

#### List Users
`GET /api/auth/users`
- Requires `admin:users` permission

#### Create User
`POST /api/auth/users`
- Requires `admin:users` permission
- Can create users with any role

#### Update User
`PUT /api/auth/users/{username}`
- Requires `admin:users` permission
- Update user details and roles

#### Delete User
`DELETE /api/auth/users/{username}`
- Requires `admin:users` permission

### API Key Management

#### Generate API Key
`POST /api/auth/generate-api-key`
- Requires authentication
- Generate long-lived API keys
- Permissions limited to user's role

Request:
```json
{
    "key_name": "Production API Key",
    "permissions": ["read:calculations", "read:exports"]
}
```

## Permissions

### Permission Format
Permissions follow the format: `action:resource`

### Available Permissions

#### Admin Permissions
- `read:all` - Read access to everything
- `write:all` - Write access to everything
- `delete:all` - Delete access to everything
- `admin:users` - User management
- `admin:settings` - System settings

#### Calculation Permissions
- `read:calculations` - View calculations
- `write:calculations` - Create/modify calculations

#### Report Permissions
- `read:reports` - View reports
- `write:reports` - Generate reports

#### Export Permissions
- `read:exports` - View exports
- `write:exports` - Create exports

## Security Best Practices

### 1. Token Management
- Store tokens securely (never in localStorage)
- Use HTTPS in production
- Implement token rotation
- Clear tokens on logout

### 2. Password Policy
- Minimum 8 characters
- Use strong passwords
- Regular password rotation
- Never share credentials

### 3. API Keys
- Generate unique keys per application
- Limit permissions to minimum required
- Rotate keys regularly
- Never commit keys to version control

### 4. Production Security
- Change default admin password
- Use environment variables for SECRET_KEY
- Implement rate limiting
- Enable CORS restrictions
- Use HTTPS only
- Monitor failed login attempts

## Implementation Examples

### Python Example
```python
import requests

# Login
response = requests.post("http://localhost:8000/api/auth/login", json={
    "username": "analyst1",
    "password": "secure_password"
})
tokens = response.json()["data"]

# Use protected endpoint
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
npv_response = requests.post(
    "http://localhost:8000/api/financial/npv",
    json={
        "cash_flows": [100000, 120000, 140000],
        "discount_rate": 0.10,
        "initial_investment": 300000
    },
    headers=headers
)
```

### JavaScript Example
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        username: 'analyst1',
        password: 'secure_password'
    })
});
const tokens = await loginResponse.json();

// Use protected endpoint
const npvResponse = await fetch('http://localhost:8000/api/financial/npv', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${tokens.data.access_token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        cash_flows: [100000, 120000, 140000],
        discount_rate: 0.10,
        initial_investment: 300000
    })
});
```

### Using API Keys
```python
# Generate API key (one-time)
api_key = generate_api_key("Production App", ["read:calculations"])

# Use API key instead of login
headers = {"Authorization": f"Bearer {api_key}"}
response = requests.get(
    "http://localhost:8000/api/financial/cache-stats",
    headers=headers
)
```

## Error Handling

### Common Error Responses

#### 401 Unauthorized
```json
{
    "status": "error",
    "code": 401,
    "message": "Invalid or expired token"
}
```

#### 403 Forbidden
```json
{
    "status": "error",
    "code": 403,
    "message": "Permission denied. Required: admin:users"
}
```

#### 400 Bad Request
```json
{
    "status": "error",
    "code": 400,
    "message": "Username already registered"
}
```

## Testing Authentication

Use the provided example client:
```bash
python examples/auth_client.py
```

This demonstrates:
- User login
- Token refresh
- Protected endpoint access
- Role-based permissions
- API key generation

## Environment Variables

Configure in production:
```bash
# JWT Secret Key (generate a strong random key)
JWT_SECRET_KEY=your-very-secure-secret-key-here

# Token expiration times
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Migration Guide

### Adding Authentication to Existing Endpoints

1. Import dependencies:
```python
from .auth_endpoints import get_current_user, require_permission, TokenData
```

2. Add authentication:
```python
@app.post("/api/endpoint")
async def endpoint(
    request: RequestModel,
    current_user: TokenData = Depends(get_current_user)
):
    # Endpoint is now protected
```

3. Add permission requirements:
```python
@app.post("/api/admin-endpoint")
async def admin_endpoint(
    request: RequestModel,
    current_user: TokenData = Depends(require_permission("admin:users"))
):
    # Only admins can access
```

## Troubleshooting

### "Invalid or expired token"
- Token has expired (30 min lifetime)
- Use refresh token to get new access token

### "Permission denied"
- User role doesn't have required permission
- Check user permissions with `/api/auth/permissions`

### "User not found"
- Username doesn't exist
- Check username spelling

### "Invalid old password"
- Current password incorrect when changing password
- Reset password through admin if needed

## Future Enhancements

1. **OAuth2 Integration**
   - Google/GitHub/Microsoft login
   - SAML support

2. **Advanced Security**
   - Two-factor authentication (2FA)
   - IP whitelisting
   - Session management

3. **Audit Logging**
   - Track all authentication events
   - Failed login monitoring
   - Permission usage tracking

4. **Enhanced User Management**
   - User groups
   - Custom roles
   - Delegated administration