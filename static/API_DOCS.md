# Swagger API Documentation for AdGenius AI

This file provides API documentation using OpenAPI 3.0 specification.

## Setup

The Swagger UI is available at: `http://localhost:5000/api/docs`

## API Documentation

For complete API documentation, please refer to the interactive Swagger UI after starting the application.

### Main Endpoints:

1. **Authentication** (`/api/v1/auth`)
   - POST /register - Register new user
   - POST /login - User login
   - POST /logout - User logout
   - GET /me - Get current user info

2. **Campaigns** (`/api/v1/campaigns`)
   - GET / - List all campaigns
   - POST / - Create new campaign
   - GET /{id} - Get campaign details
   - PUT /{id} - Update campaign
   - DELETE /{id} - Delete campaign

3. **Analytics** (`/api/v1/analytics`)
   - GET /campaigns/{id} - Get campaign analytics
   - GET /dashboard - Get dashboard summary

4. **Users** (`/api/v1/users`)
   - GET / - List users (admin only)
   - GET /{id} - Get user details
   - PUT /{id} - Update user
   - DELETE /{id} - Delete user

## Full API Documentation

To generate a complete swagger.json file, run:

```bash
python generate_swagger.py
```

This will create a comprehensive OpenAPI specification file.
