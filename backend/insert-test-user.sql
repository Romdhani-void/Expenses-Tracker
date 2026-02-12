-- Insert test user with specific UUID for hardcoded backend
INSERT INTO users (id, email, password, name)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'test@example.com',
  'password123',
  'Test User'
)
ON CONFLICT (id) DO NOTHING;

SELECT * FROM users WHERE id = '00000000-0000-0000-0000-000000000001';
