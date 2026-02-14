# Expense Tracker - Architecture Documentation

## Overview

The Expense Tracker application is built using a microservices architecture with clear separation of concerns. Each service is independently deployable and scalable, communicating via RESTful APIs through a central API Gateway.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         React Frontend                          │
│                      (http://localhost:3000)                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API Gateway (Nginx)                       │
│                     (http://localhost:8080)                      │
│                                                                 │
│  Routes:                                                        │
│  /api/auth/*         → Auth Service                            │
│  /api/budgets/*      → Budget Service                          │
│  /api/categories/*   → Budget Service                          │
│  /api/transactions/* → Transaction Service                    │
│  /api/analytics/*    → Analytics Service                       │
└─────────────────────────────────────────────────────────────────┘
            │              │              │              │
            ▼              ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│     Auth     │ │    Budget    │ │ Transaction  │ │  Analytics   │
│   Service    │ │   Service    │ │   Service    │ │   Service    │
│  (Node.js)   │ │  (Node.js)   │ │  (Python)    │ │  (Python)    │
│   Port 3001  │ │   Port 3002  │ │   Port 3003  │ │   Port 3004  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │                │
       ▼                ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │  PostgreSQL  │ │   MongoDB    │ │    Redis     │
│  (Auth DB)   │ │ (Budget DB)  │ │(Transactions)│ │   (Cache)    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Ports:**

- **Backend exposed at:** Port **8080** (API Gateway Nginx). All API requests go to `http://localhost:8080/api/*`; the gateway routes to Auth (3001), Budget (3002), Transaction (3003), Analytics (3004). Ports 3001–3004 are internal.
- **Frontend exposed at:** Port **80** (Frontend Nginx). Serves the built React app and proxies `/api/*` to 8080, so one URL (e.g. `http://localhost`) serves the UI and API. Config: [frontend/nginx.conf](frontend/nginx.conf). In development, the frontend runs on 3000 (Vite) and can proxy to 3001–3004 or to 8080.

## Service Responsibilities

### 1. Auth Service (Node.js + PostgreSQL)

**Port:** 3001  
**Responsibilities:**

- User registration and authentication
- Email/password login
- Google OAuth 2.0 integration
- JWT token generation and validation
- Session management

**Database:** PostgreSQL (`expense_tracker_auth`)

- Users table with credentials and OAuth info

**External Dependencies:**

- Google OAuth API

---

### 2. Budget Service (Node.js + PostgreSQL)

**Port:** 3002  
**Responsibilities:**

- Create and manage monthly budgets
- Define spending categories
- Set planned amounts per category
- Track opening/closing balances
- Support multiple currencies
- Handle recurring category templates

**Database:** PostgreSQL (`expense_tracker_budget`)

- Budgets table (monthly budgets)
- Budget categories table (category limits)

**No external service dependencies**

---

### 3. Transaction Service (Python + MongoDB)

**Port:** 3003  
**Responsibilities:**

- Track income transactions
- Track expense transactions
- CRUD operations on transactions
- Filter transactions by date, category, type
- Generate category summaries
- Multi-currency transaction support

**Database:** MongoDB (`expense_tracker_transactions`)

- Transactions collection

**No external service dependencies**

---

### 4. Analytics Service (Python + Redis)

**Port:** 3004  
**Responsibilities:**

- Calculate monthly income and expenses
- Compute closing balances
- Compare budget vs actual spending
- Generate category-wise spending reports
- Calculate real available money (closing - saves)
- Provide monthly trends
- Cache calculation results

**Cache:** Redis

- TTL-based caching for expensive calculations

**External Service Dependencies:**

- Transaction Service (fetch transaction data)
- Budget Service (fetch budget data)

---

### 5. API Gateway (Nginx)

**Port:** 8080  
**Responsibilities:**

- Single entry point for all API requests
- Route requests to appropriate microservices
- Handle CORS
- (Future: Rate limiting, auth middleware)

**No database**

---

## Data Flow

### 1. Authentication Flow

```
1. User → Frontend: Enter credentials
2. Frontend → API Gateway → Auth Service: POST /api/auth/login
3. Auth Service → PostgreSQL: Validate credentials
4. Auth Service ← PostgreSQL: User data
5. Auth Service: Generate JWT token
6. Frontend ← API Gateway ← Auth Service: Return JWT token
7. Frontend: Store token in localStorage
8. All subsequent requests: Include "Authorization: Bearer {token}"
```

### 2. Creating a Budget Flow

```
1. Frontend → API Gateway → Auth Service: Validate JWT
2. Frontend → API Gateway → Budget Service: POST /api/budgets
   Headers: Authorization: Bearer {token}
   Body: { year, month, currency, opening_balance }
3. Budget Service: Validate JWT (extract user_id)
4. Budget Service → PostgreSQL: Insert budget
5. Frontend ← Budget Service: Budget created
```

### 3. Adding a Transaction Flow

```
1. Frontend → API Gateway → Transaction Service: POST /api/transactions
   Headers: Authorization: Bearer {token}
   Body: { type, amount, currency, category, date, notes }
2. Transaction Service: Validate JWT
3. Transaction Service → MongoDB: Insert transaction
4. Frontend ← Transaction Service: Transaction created
```

### 4. Analytics Calculation Flow

```
1. Frontend → API Gateway → Analytics Service: GET /api/analytics/month/2026/2
2. Analytics Service: Check Redis cache
3. If cached: Return cached result
4. If not cached:
   a. Analytics → Transaction Service: GET /transactions (with filters)
   b. Analytics → Budget Service: GET /budgets/month/2026/2
   c. Analytics: Perform calculations
   d. Analytics → Redis: Cache result (TTL: 5 min)
   e. Return result
```

## Database Schemas

### Auth Service (PostgreSQL)

**users table:**

```sql
- id (UUID, PK)
- email (VARCHAR, UNIQUE)
- password (VARCHAR, nullable for OAuth users)
- name (VARCHAR)
- google_id (VARCHAR, nullable)
- created_at (TIMESTAMP)
```

### Budget Service (PostgreSQL)

**budgets table:**

```sql
- id (UUID, PK)
- user_id (UUID)
- year (INTEGER)
- month (INTEGER)
- currency (VARCHAR)
- opening_balance (DECIMAL)
- closing_balance (DECIMAL)
- created_at, updated_at (TIMESTAMP)
- UNIQUE(user_id, year, month)
```

**budget_categories table:**

```sql
- id (UUID, PK)
- budget_id (UUID, FK → budgets.id)
- name (VARCHAR)
- planned_amount (DECIMAL)
- actual_amount (DECIMAL)
- currency (VARCHAR)
- is_recurring (BOOLEAN)
- recurring_amount (DECIMAL)
- created_at, updated_at (TIMESTAMP)
- UNIQUE(budget_id, name)
```

### Transaction Service (MongoDB)

**transactions collection:**

```json
{
  "_id": ObjectId,
  "user_id": "UUID",
  "type": "income" | "expense",
  "amount": Number,
  "currency": "USD",
  "category": "Category Name",
  "date": "ISO Date",
  "notes": "Optional",
  "created_at": "ISO DateTime",
  "updated_at": "ISO DateTime"
}
```

## Authentication & Authorization

### JWT Token Structure

```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "User Name",
  "iat": 1234567890,
  "exp": 1234567890
}
```

### Token Flow

1. **Auth Service** generates JWT after successful login
2. **Frontend** stores token in localStorage
3. **All requests** include token in `Authorization: Bearer {token}` header
4. **Each service** validates token independently using shared `JWT_SECRET`
5. Services extract `user_id` from token to filter data by user

### Security Considerations

- JWT secret must be shared across all services (via environment variables)
- Tokens expire after configurable period (default: 7 days)
- Passwords hashed with bcrypt (10 salt rounds)
- HTTPS recommended for production
- CORS configured to allow frontend origin only

## Inter-Service Communication

### Current: Synchronous HTTP

- Analytics Service calls Transaction and Budget services via HTTP
- Simple, straightforward implementation
- Good for read operations

### Future: Asynchronous with RabbitMQ

Potential message queue scenarios:

- **Transaction created** → Update budget actual_amount
- **Budget updated** → Invalidate analytics cache
- **User registered** → Send welcome email
- **Monthly summary** → Generate and email report

## Caching Strategy

### Analytics Service (Redis)

- **Cache Key Pattern:** `analytics:{md5(user_id:endpoint:params)}`
- **TTL:** 5 minutes (configurable)
- **Invalidation:** Time-based (TTL) or explicit on data changes

### Cache Examples:

```
analytics:abc123... → Monthly summary for user X, Feb 2026
analytics:def456... → Category summary for user Y, Q1 2026
```

## Scalability Considerations

### Horizontal Scaling

Each service can be scaled independently:

- **Auth Service:** Stateless, easy to scale (add load balancer)
- **Budget Service:** Stateless, database becomes bottleneck
- **Transaction Service:** Stateless, MongoDB can be sharded
- **Analytics Service:** Stateless, Redis can be clustered

### Database Scaling

- **PostgreSQL:** Read replicas for read-heavy queries
- **MongoDB:** Sharding by user_id for horizontal scaling
- **Redis:** Redis Cluster for distributed caching

### Load Balancing

Add load balancer in front of API Gateway:

```
Load Balancer → Multiple API Gateway instances → Services
```

## Deployment Architecture

### Development

- All services run on localhost with different ports
- Single machine setup

### Production (Recommended)

```
Internet
  ↓
Load Balancer (HTTPS)
  ↓
API Gateway (Nginx) x N instances
  ↓
Service Mesh / K8s Cluster
  ├── Auth Service (x M replicas)
  ├── Budget Service (x N replicas)
  ├── Transaction Service (x P replicas)
  └── Analytics Service (x Q replicas)
  ↓
Managed Databases
  ├── PostgreSQL (Primary + Replicas)
  ├── MongoDB (Replica Set)
  └── Redis (Cluster)
```

## Monitoring & Observability

Recommended additions:

- **Logging:** Centralized logging (ELK Stack, CloudWatch)
- **Metrics:** Prometheus + Grafana
- **Tracing:** Distributed tracing (Jaeger, Zipkin)
- **Health Checks:** Each service has `/health` endpoint
- **Alerts:** Set up alerts for service downtime, high error rates

## Technology Choices Rationale

### Why Node.js for Auth & Budget?

- Fast, non-blocking I/O
- Large ecosystem
- Well-suited for API servers
- Easy integration with PostgreSQL

### Why Python for Transaction & Analytics?

- Excellent for data processing
- Rich analytics libraries
- Clean syntax for business logic
- Good MongoDB and Redis support

### Why PostgreSQL for Auth & Budget?

- ACID compliance for critical user data
- Strong relational model for budgets/categories
- Proven reliability

### Why MongoDB for Transactions?

- Flexible schema for varying transaction types
- High write throughput
- Easy to scale horizontally
- Good for time-series data

### Why Redis for Analytics?

- In-memory speed for frequent calculations
- TTL-based expiration
- Simple key-value caching
- Low latency

### Why Nginx for Gateway?

- Industry standard
- High performance
- Easy configuration
- Mature and reliable

## Future Enhancements

1. **Message Queue:** RabbitMQ for async communication
2. **Email Service:** Notification and reports
3. **File Upload Service:** Receipt/document storage
4. **Notification Service:** Real-time alerts
5. **Export Service:** PDF/Excel report generation
6. **Admin Dashboard:** System monitoring and management
7. **Mobile App:** React Native frontend
8. **GraphQL Gateway:** Alternative to REST

## Conclusion

This microservices architecture provides:

- ✅ Clear separation of concerns
- ✅ Independent scalability
- ✅ Technology diversity (polyglot)
- ✅ Resilience (service isolation)
- ✅ Easier testing and deployment
- ✅ Team autonomy (different teams can own different services)
