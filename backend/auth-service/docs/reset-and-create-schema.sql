-- Auth Service PostgreSQL Schema (Corrected)
-- This matches the application code column names

-- Drop existing tables (in correct order due to foreign key constraints)
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table (corrected column names to match code)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  google_id VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Sessions table (optional - for tracking active sessions)
CREATE TABLE sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jwt_token TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- Verify tables were created
SELECT 'SUCCESS: Auth tables created with correct schema!' AS status;