# Expense Tracker - Microservices Architecture

A personal expense tracker application built with microservices architecture, featuring multi-currency support, budget planning, and analytics.

## Architecture Overview

This application consists of 5 independent microservices:

1. **Auth Service** (Node.js + PostgreSQL) - User authentication with JWT and Google OAuth
2. **Budget Service** (Node.js + PostgreSQL) - Monthly budget management and categories
3. **Transaction Service** (Python + MongoDB) - Income and expense tracking
4. **Analytics Service** (Python + Redis) - Calculations, trends, and insights
5. **API Gateway** (Nginx) - Single entry point routing requests to services

Plus a **React Frontend** for the UI.

**Tech stack (per prompt):** Auth & Budget: Node.js, Express, Postgres, Passport.js (Auth only). Transaction: Python, Flask, MongoDB. Analytics: Python, Flask, Redis. API Gateway: Nginx (or Kong). Frontend: React, Axios. Optional: RabbitMQ for async communication.

## Features

- ✅ User authentication (Email/Password + Google OAuth)
- ✅ Session-based JWT protection
- ✅ Multi-currency support (USD, CAD, HUF, EUR, etc.)
- ✅ Monthly budget planning with customizable categories
- ✅ Income and expense tracking
- ✅ Budget vs actual spending comparison
- ✅ Monthly trends and analytics
- ✅ Recurring category auto-fill
- ✅ Real available money calculation (closing balance - saves)

## Project Structure

```
expense-tracker/
├── backend/
│   ├── auth-service/          # Authentication microservice (Node.js + PostgreSQL)
│   │   ├── src/
│   │   ├── docs/
│   │   ├── package.json
│   │   └── README.md
│   ├── budget-service/        # Budget management microservice (Node.js + PostgreSQL)
│   │   ├── src/
│   │   ├── docs/
│   │   ├── package.json
│   │   └── README.md
│   ├── transaction-service/   # Transaction tracking microservice (Python + MongoDB)
│   │   ├── routes/
│   │   ├── models/
│   │   ├── docs/
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── analytics-service/     # Analytics microservice (Python + Redis)
│   │   ├── routes/
│   │   ├── services/
│   │   ├── requirements.txt
│   │   └── README.md
│   └── api-gateway/          # Nginx API Gateway
│       ├── nginx.conf
│       └── README.md
└── frontend/             # React frontend
    ├── src/
    ├── package.json
    └── README.md
```

## Prerequisites

- **Node.js** (v14+) – Auth and Budget services
- **Python** (v3.8+) – Transaction and Analytics services
- **Docker** – to run database images (PostgreSQL, MongoDB, Redis). No local DB installation.
- **Nginx** (optional) – API Gateway; in dev the frontend proxy can target services directly.

## Quick Start

### 1. Clone and enter project

```bash
git clone <repository-url>
cd "Expense Tracker"
```

### 2. Run databases (Docker images only)

Run PostgreSQL, MongoDB, and Redis via Docker. See **[backend/DATABASE-SETUP.md](backend/DATABASE-SETUP.md)** for exact `docker run` commands and schema steps. After that, the app connects to `localhost` (ports 5432, 27017, 6379).

### 3. Configure Environment Variables

Each service has a `.env.example` file. Copy to `.env` and update:

```bash
# Auth Service
cd backend/auth-service
cp .env.example .env
# Edit .env with your database credentials

# Budget Service
cd ../budget-service
cp .env.example .env
# Edit .env

# Transaction Service
cd ../transaction-service
cp .env.example .env
# Edit .env

# Analytics Service
cd ../analytics-service
cp .env.example .env
# Edit .env
```

**Important:** All services must use the same `JWT_SECRET`.

### 4. Install Dependencies

**Node.js services:**

```bash
cd backend/auth-service && npm install
cd ../../budget-service && npm install
```

**Python services:**

```bash
cd backend/transaction-service && pip install -r requirements.txt
cd ../../analytics-service && pip install -r requirements.txt
```

**Frontend:**

```bash
cd frontend && npm install
```

### 5. Start Services

Open separate terminal windows for each service:

```bash
# Terminal 1: Auth Service
cd backend/auth-service
npm run dev              # Runs on port 3001

# Terminal 2: Budget Service
cd backend/budget-service
npm run dev              # Runs on port 3002

# Terminal 3: Transaction Service
cd backend/transaction-service
python app.py            # Runs on port 3003

# Terminal 4: Analytics Service
cd backend/analytics-service
python app.py            # Runs on port 3004

# Terminal 5: API Gateway
nginx -c <full-path-to>/backend/api-gateway/nginx.conf
# Or use system nginx with the config    # Runs on port 8080

# Terminal 6: Frontend
cd frontend
npm run dev              # Runs on port 3000
```

### 6. Access the Application

Open your browser and navigate to:

```
http://localhost:3000
```

## Service Ports

| Port | Service                  | Description                                      |
| ---- | ------------------------ | ------------------------------------------------ |
| 3000 | Frontend (dev)           | Vite dev server (development only)               |
| 3001 | Auth Service             | Authentication & JWT                             |
| 3002 | Budget Service           | Budgets & Categories                             |
| 3003 | Transaction Service      | Income & Expenses                                |
| 3004 | Analytics Service        | Calculations & Trends                             |
| **80**  | **Frontend (Nginx)** | **Where the frontend is exposed** (serves built React app; proxies `/api` → 8080) |
| **8080** | **API Gateway**     | **Where the backend is exposed** (single entry point; routes to 3001–3004) |

**Two Nginx roles:**

- **Backend (port 8080):** [backend/api-gateway/nginx.conf](backend/api-gateway/nginx.conf) — API Gateway. All API traffic goes to `http://localhost:8080/api/*` and is routed to Auth (3001), Budget (3002), Transaction (3003), Analytics (3004).
- **Frontend (port 80):** [frontend/nginx.conf](frontend/nginx.conf) — Serves the built React app (`npm run build` → `dist/`). Proxies `/api/*` to `http://127.0.0.1:8080`, so users open one URL (e.g. `http://localhost`) for the app and API. Use `root` / path to your `frontend/dist` when running Nginx on the host.

## Service Documentation

Each service has its own README and API documentation:

- [Auth Service](backend/auth-service/README.md) - [API Docs](backend/auth-service/docs/api.md)
- [Budget Service](backend/budget-service/README.md) - [API Docs](backend/budget-service/docs/api.md)
- [Transaction Service](backend/transaction-service/README.md) - [API Docs](backend/transaction-service/docs/api.md)
- [Analytics Service](backend/analytics-service/README.md)
- [API Gateway](backend/api-gateway/README.md)
- [Frontend](frontend/README.md)

## API Gateway Routes (backend exposed on 8080)

With the gateway running, the **entire backend** is reached at `http://localhost:8080`. The frontend calls `/api/...` and the gateway forwards:

- `/api/auth/*` → Auth Service (3001)
- `/api/budgets/*` → Budget Service (3002)
- `/api/categories/*` → Budget Service (3002)
- `/api/transactions/*` → Transaction Service (3003)
- `/api/analytics/*` → Analytics Service (3004)

## Architecture Details

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation including:

- Service interactions
- Data flow
- Authentication flow
- Database relationships
- Scalability considerations

## Development Workflow

1. Start all backend services in development mode
2. Start the API Gateway
3. Start the frontend with hot reload
4. Frontend proxy forwards `/api/*` requests to the gateway
5. Make changes and test

## Testing

Each service can be tested individually:

```bash
# Test Auth Service
curl -X POST http://localhost:3001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123","name":"Test"}'

# Test through API Gateway
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"password123","name":"Test"}'
```

## Troubleshooting

### Service won't start

- Check if required dependencies are installed
- Verify database connections
- Ensure ports are not in use
- Check `.env` configuration

### Database connection errors

- Verify PostgreSQL/MongoDB/Redis are running
- Check credentials in `.env` files
- Ensure databases exist

### JWT token errors

- Verify `JWT_SECRET` is the same across all services
- Check token expiration settings
- Ensure Authorization header format is correct

### CORS errors

- Verify API Gateway CORS configuration
- Check frontend proxy settings
- Ensure services allow CORS from gateway

## Production

Set `NODE_ENV=production`, use environment variables for secrets, configure CORS and SSL as needed. Use process managers (e.g. PM2 for Node, systemd for Python) to run services.

## RabbitMQ (optional)

The design supports async communication via RabbitMQ (e.g. budget/transaction events, analytics recalculation). See [backend/DATABASE-SETUP.md](backend/DATABASE-SETUP.md) for an optional RabbitMQ container.

## License

MIT

## Contributing

Contributions are welcome! Please read the contribution guidelines before submitting PRs.

## Support

For issues and questions, please open an issue in the repository.
