# Auth Service

Authentication microservice for the Expense Tracker application. Handles user registration, login, Google OAuth, and JWT token management.

## Features

- ✅ Email/password registration and login
- ✅ Google OAuth 2.0 authentication
- ✅ JWT token generation and validation
- ✅ Session management
- ✅ Password hashing with bcrypt
- ✅ Secure token-based authentication

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** PostgreSQL
- **Authentication:** Passport.js (Local + Google OAuth)
- **Token:** JWT (jsonwebtoken)
- **Password Hashing:** bcrypt

## Prerequisites

- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)
- Google OAuth credentials (optional, for Google login)

## Setup

### 1. Install Dependencies

```bash
cd auth-service
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
PORT=3001
NODE_ENV=development
FRONTEND_URL=http://localhost:3000

DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_tracker_auth
DB_USER=postgres
DB_PASSWORD=your_password

JWT_SECRET=your-secret-key-change-this
JWT_EXPIRES_IN=7d

SESSION_SECRET=your-session-secret-change-this

# Optional: For Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_CALLBACK_URL=http://localhost:3001/auth/google/callback
```

### 3. Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE expense_tracker_auth;

# Connect to the database
\c expense_tracker_auth

# Run the schema
\i docs/schema.sql
```

Or simply:

```bash
psql -U postgres -c "CREATE DATABASE expense_tracker_auth;"
psql -U postgres -d expense_tracker_auth -f docs/schema.sql
```

### 4. Run the Service

**Development mode (with auto-reload):**

```bash
npm run dev
```

**Production mode:**

```bash
npm start
```

The service will start on `http://localhost:3001`

## API Documentation

See [docs/api.md](docs/api.md) for complete API documentation.

## Google OAuth Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:3001/auth/google/callback`
6. Copy Client ID and Client Secret to `.env`

## Testing

### Test Registration

```bash
curl -X POST http://localhost:3001/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'
```

### Test Login

```bash
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Token Validation

```bash
curl -X GET http://localhost:3001/auth/validate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

The service uses a single `users` table:

| Column     | Type         | Description                                |
| ---------- | ------------ | ------------------------------------------ |
| id         | UUID         | Primary key                                |
| email      | VARCHAR(255) | Unique email address                       |
| password   | VARCHAR(255) | Hashed password (nullable for OAuth users) |
| name       | VARCHAR(255) | User's display name                        |
| google_id  | VARCHAR(255) | Google OAuth ID (nullable)                 |
| created_at | TIMESTAMPTZ  | Account creation timestamp                 |

## Security Considerations

- Passwords are hashed using bcrypt with 10 salt rounds
- JWT tokens expire after 7 days (configurable)
- Sessions use secure cookies in production
- CORS is configured to only allow requests from the frontend URL
- All sensitive data is stored in environment variables

## Troubleshooting

**Database connection errors:**

- Verify PostgreSQL is running: `pg_isready`
- Check database credentials in `.env`
- Ensure database exists

**Google OAuth not working:**

- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set
- Check redirect URI matches in Google Cloud Console
- Ensure Google+ API is enabled

## License

MIT
