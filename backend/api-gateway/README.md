# API Gateway

Nginx-based API Gateway for the Expense Tracker microservices application.

## Purpose

The API Gateway serves as a single entry point for the frontend, routing requests to the appropriate microservices:

- Auth Service (port 3001)
- Budget Service (port 3002)
- Transaction Service (port 3003)
- Analytics Service (port 3004)

## Setup

### 1. Install Nginx

**Windows:**

- Download from [nginx.org](https://nginx.org/en/download.html)
- Extract to a directory

**macOS:**

```bash
brew install nginx
```

**Linux:**

```bash
sudo apt-get install nginx  # Ubuntu/Debian
sudo yum install nginx      # CentOS/RHEL
```

### 2. Configure Nginx

Copy the `nginx.conf` file to your Nginx configuration directory:

**Windows:**

- Replace `conf/nginx.conf` in your Nginx installation directory

**macOS/Linux:**

```bash
sudo cp nginx.conf /etc/nginx/nginx.conf
# Or create a site configuration
sudo cp nginx.conf /etc/nginx/sites-available/expense-tracker
sudo ln -s /etc/nginx/sites-available/expense-tracker /etc/nginx/sites-enabled/
```

### 3. Start Nginx

**Windows:**

```bash
nginx.exe
```

**macOS:**

```bash
brew services start nginx
# Or
sudo nginx
```

**Linux:**

```bash
sudo systemctl start nginx
# Or
sudo nginx
```

### 4. Verify

Check if the gateway is running:

```bash
curl http://localhost:8080/health
```

Should return: `Gateway is healthy`

## API Routes

All microservices are accessible through port 8080:

| Service     | Original Port | Gateway Route        | Example                     |
| ----------- | ------------- | -------------------- | --------------------------- |
| Auth        | 3001          | /api/auth/\*         | /api/auth/register          |
| Budget      | 3002          | /api/budgets/\*      | /api/budgets                |
| Budget      | 3002          | /api/categories/\*   | /api/categories             |
| Transaction | 3003          | /api/transactions/\* | /api/transactions           |
| Analytics   | 3004          | /api/analytics/\*    | /api/analytics/month/2026/2 |

## Example Usage

### From Frontend

```javascript
// Instead of calling services directly:
// http://localhost:3001/auth/login

// Use the gateway:
const response = await fetch("http://localhost:8080/api/auth/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ email, password }),
});
```

### Testing with curl

```bash
# Register user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123","name":"Test User"}'

# Get budgets
curl http://localhost:8080/api/budgets \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get transactions
curl http://localhost:8080/api/transactions \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get analytics
curl http://localhost:8080/api/analytics/month/2026/2 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## CORS Configuration

CORS is configured to allow all origins for development:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Authorization, Content-Type`

For production, update the CORS configuration to only allow your frontend domain.

## Troubleshooting

**Nginx won't start:**

- Check if port 8080 is already in use
- Verify nginx configuration: `nginx -t`
- Check error logs

**Services not responding:**

- Ensure all microservices are running on their respective ports
- Check service health endpoints directly
- Verify upstream configuration in nginx.conf

**CORS errors:**

- Verify CORS headers are being sent
- Check browser console for specific errors
- Ensure preflight requests (OPTIONS) are handled

## Reload Configuration

After making changes to `nginx.conf`:

**Windows:**

```bash
nginx.exe -s reload
```

**macOS/Linux:**

```bash
sudo nginx -s reload
```

## Stop Nginx

**Windows:**

```bash
nginx.exe -s stop
```

**macOS:**

```bash
brew services stop nginx
# Or
sudo nginx -s stop
```

**Linux:**

```bash
sudo systemctl stop nginx
# Or
sudo nginx -s stop
```

## Production Considerations

For production deployment:

1. Enable SSL/TLS
2. Restrict CORS to specific domains
3. Add rate limiting
4. Enable request logging
5. Add authentication middleware
6. Configure timeouts appropriately
7. Enable gzip compression
8. Set up health checks for upstream services

## License

MIT
