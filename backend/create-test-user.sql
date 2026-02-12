-- Create a test user for the Expense Tracker application
-- Password: 'password123' (hashed using bcrypt with 10 salt rounds)

INSERT INTO users (email, password, name)
VALUES (
  'test@example.com',
  '$2b$10$rBV2X3dP5fzqKpB7fNZ4juEhY4Y4uwRn2mHJQH5z5I5K5K5K5K5K5K',
  'Test User'
);

-- Verify the user was created
SELECT id, email, name, created_at FROM users;
