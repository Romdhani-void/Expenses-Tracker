# Auth Service API Documentation

Base URL: `http://localhost:3001`

## Authentication Endpoints

### 1. Register User

**POST** `/auth/register`

Register a new user with email and password.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

- `400 Bad Request`: Missing required fields or password too short
- `409 Conflict`: Email already registered

---

### 2. Login

**POST** `/auth/login`

Authenticate with email and password.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**

```json
{
  "message": "Login successful",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid credentials

---

### 3. Google OAuth Login

**GET** `/auth/google`

Initiates Google OAuth flow. Redirects to Google login page.

**Response:**
Redirects to Google OAuth consent screen.

---

### 4. Google OAuth Callback

**GET** `/auth/google/callback`

Callback URL for Google OAuth. Automatically handled by Passport.

**Response:**
Redirects to frontend with token: `{FRONTEND_URL}/auth/callback?token={JWT_TOKEN}`

---

### 5. Validate Token

**GET** `/auth/validate`

Validates a JWT token.

**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "valid": true,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid or expired token

---

### 6. Logout

**POST** `/auth/logout`

Logs out the current user (clears session).

**Response (200 OK):**

```json
{
  "message": "Logged out successfully"
}
```

---

### 7. Health Check

**GET** `/health`

Check if the service is running.

**Response (200 OK):**

```json
{
  "status": "ok",
  "service": "auth-service"
}
```

---

## Authentication Flow

### Email/Password Flow:

1. User registers via `/auth/register` or logs in via `/auth/login`
2. Server returns JWT token
3. Client stores token (localStorage/sessionStorage)
4. Client includes token in `Authorization` header for subsequent requests to other services

### Google OAuth Flow:

1. User clicks "Login with Google" → Frontend redirects to `/auth/google`
2. User authenticates with Google
3. Google redirects to `/auth/google/callback`
4. Server generates JWT and redirects to frontend with token
5. Frontend extracts token from URL and stores it

---

## JWT Token Format

The JWT token contains the following payload:

```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1234567890,
  "exp": 1234567890
}
```

**Token Expiration:** 7 days (configurable via `JWT_EXPIRES_IN`)

---

## Error Handling

All errors follow this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:

- `400`: Bad Request (validation errors)
- `401`: Unauthorized (authentication failed)
- `403`: Forbidden (invalid token)
- `409`: Conflict (duplicate email)
- `500`: Internal Server Error
