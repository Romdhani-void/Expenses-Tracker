# Budget Service

Budget management microservice for the Expense Tracker application. Handles monthly budgets, spending categories, and multi-currency support.

## Features

- ✅ Monthly budget creation and management
- ✅ Customizable spending categories
- ✅ Multi-currency support (USD, CAD, HUF, EUR, etc.)
- ✅ Opening and closing balance tracking
- ✅ Recurring category auto-fill
- ✅ Budget vs actual spending limits
- ✅ Month-to-month budget carryover

## Tech Stack

- **Runtime:** Node.js
- **Framework:** Express.js
- **Database:** PostgreSQL
- **Authentication:** JWT validation

## Prerequisites

- Node.js (v14 or higher)
- PostgreSQL (v12 or higher)
- Valid JWT secret (must match Auth Service)

## Setup

### 1. Install Dependencies

```bash
cd budget-service
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
```

Edit `.env`:

```env
PORT=3002
DB_HOST=localhost
DB_PORT=5432
DB_NAME=expense_tracker_budget
DB_USER=postgres
DB_PASSWORD=your_password
JWT_SECRET=same-secret-as-auth-service
```

**Important:** `JWT_SECRET` must match the Auth Service secret.

### 3. Create Database

```bash
# Create database
psql -U postgres -c "CREATE DATABASE expense_tracker_budget;"

# Run schema
psql -U postgres -d expense_tracker_budget -f docs/schema.sql
```

### 4. Run the Service

**Development mode:**

```bash
npm run dev
```

**Production mode:**

```bash
npm start
```

Service runs on `http://localhost:3002`

## API Documentation

See [docs/api.md](docs/api.md) for complete API documentation.

## Quick Start Example

### 1. Create a Monthly Budget

```bash
curl -X POST http://localhost:3002/budgets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2026,
    "month": 2,
    "currency": "USD",
    "opening_balance": 5000
  }'
```

### 2. Add Categories

```bash
curl -X POST http://localhost:3002/categories/bulk \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "budget_id": "your-budget-uuid",
    "categories": [
      {
        "name": "Rent",
        "currency": "USD",
        "is_recurring": true,
        "recurring_amount": 1200
      },
      {
        "name": "Groceries",
        "currency": "USD",
        "is_recurring": true,
        "recurring_amount": 400
      }
    ]
  }'
```

### 3. Get Budget with Categories

```bash
curl -X GET http://localhost:3002/budgets/month/2026/2 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

### budgets Table

| Column          | Type          | Description              |
| --------------- | ------------- | ------------------------ |
| id              | UUID          | Primary key              |
| user_id         | UUID          | User who owns the budget |
| year            | INTEGER       | Budget year              |
| month           | INTEGER       | Budget month (1-12)      |
| currency        | VARCHAR(3)    | Currency code            |
| opening_balance | DECIMAL(15,2) | Starting balance         |
| closing_balance | DECIMAL(15,2) | Ending balance           |
| created_at      | TIMESTAMPTZ   | Creation timestamp       |
| updated_at      | TIMESTAMPTZ   | Last update timestamp    |

### budget_categories Table

| Column           | Type          | Description                  |
| ---------------- | ------------- | ---------------------------- |
| id               | UUID          | Primary key                  |
| budget_id        | UUID          | Foreign key to budgets       |
| name             | VARCHAR(100)  | Category name                |
| planned_amount   | DECIMAL(15,2) | Planned spending             |
| actual_amount    | DECIMAL(15,2) | Actual spending              |
| currency         | VARCHAR(3)    | Currency code                |
| is_recurring     | BOOLEAN       | Is this a recurring category |
| recurring_amount | DECIMAL(15,2) | Default amount for recurring |
| created_at       | TIMESTAMPTZ   | Creation timestamp           |
| updated_at       | TIMESTAMPTZ   | Last update timestamp        |

## Features Explained

### Recurring Categories

Mark categories as recurring to auto-fill them in future months:

- Set `is_recurring: true`
- Set `recurring_amount` to the default value
- Use bulk create to auto-generate all recurring categories for new months

### Multi-Currency Support

Each budget and category can have its own currency:

- Budget has a primary currency
- Categories can have different currencies
- Analytics Service handles currency conversion

### Balance Tracking

- `opening_balance`: Starting balance for the month
- `closing_balance`: Ending balance (opening + income - expenses)
- Closing balance of one month becomes opening balance of next month

## Integration with Other Services

- **Auth Service:** Validates JWT tokens
- **Transaction Service:** Gets actual spending amounts per category
- **Analytics Service:** Computes actual vs planned comparisons

## Troubleshooting

**Database connection errors:**

- Verify PostgreSQL is running
- Check credentials in `.env`
- Ensure database exists

**JWT validation errors:**

- Ensure `JWT_SECRET` matches Auth Service
- Check token is included in `Authorization` header
- Verify token hasn't expired

## License

MIT
