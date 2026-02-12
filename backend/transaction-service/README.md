# Transaction Service

Transaction management microservice for the Expense Tracker application. Handles income and expense tracking with MongoDB storage.

## Features

- ✅ Add income and expenses
- ✅ Edit and delete transactions
- ✅ Filter by date range and category
- ✅ Multi-currency support
- ✅ Category-based expense tracking
- ✅ Aggregated summaries by category
- ✅ MongoDB for flexible document storage

## Tech Stack

- **Language:** Python 3.8+
- **Framework:** Flask
- **Database:** MongoDB
- **Authentication:** JWT validation
- **CORS:** Flask-CORS

## Prerequisites

- Python 3.8 or higher
- MongoDB 4.0 or higher
- Valid JWT secret (must match Auth Service)

## Setup

### 1. Install Dependencies

```bash
cd transaction-service
pip install -r requirements.txt
```

Or create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env`:

```env
PORT=3003
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=expense_tracker_transactions
JWT_SECRET=same-secret-as-auth-service
FRONTEND_URL=http://localhost:3000
```

**Important:** `JWT_SECRET` must match the Auth Service.

### 3. Start MongoDB

```bash
# Start MongoDB server
mongod

# Or if using MongoDB as a service
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

### 4. Run the Service

```bash
python app.py
```

Service runs on `http://localhost:3003`

## API Documentation

See [docs/api.md](docs/api.md) for complete API documentation.

## Quick Start Example

### 1. Add Income

```bash
curl -X POST http://localhost:3003/transactions/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "income",
    "amount": 3500,
    "currency": "USD",
    "category": "Salary",
    "date": "2026-02-01"
  }'
```

### 2. Add Expense

```bash
curl -X POST http://localhost:3003/transactions/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "expense",
    "amount": 45.50,
    "currency": "USD",
    "category": "Groceries",
    "date": "2026-02-10",
    "notes": "Weekly shopping"
  }'
```

### 3. Get Transactions

```bash
# Get all transactions
curl http://localhost:3003/transactions/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Filter by date range
curl "http://localhost:3003/transactions/?start_date=2026-02-01&end_date=2026-02-28" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Filter by category
curl "http://localhost:3003/transactions/?category=Groceries" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## MongoDB Schema

See [docs/schema.md](docs/schema.md) for detailed schema documentation.

### Transaction Document

```json
{
  "_id": ObjectId,
  "user_id": "UUID",
  "type": "income" | "expense",
  "amount": Number,
  "currency": "USD",
  "category": "Category Name",
  "date": "2026-02-10T14:30:00Z",
  "notes": "Optional notes",
  "created_at": "2026-02-10T14:35:00Z",
  "updated_at": "2026-02-10T14:35:00Z"
}
```

## Features Explained

### Transaction Types

- **Income**: Money received (salary, bonuses, extra income)
- **Expense**: Money spent (rent, groceries, bills, etc.)

### Multi-Currency Support

Each transaction can have its own currency:

- USD, CAD, HUF, EUR, GBP, etc.
- Exchange rate conversion handled by Analytics Service

### Filtering

Filter transactions by:

- Date range (`start_date`, `end_date`)
- Category
- Transaction type (income/expense)
- Combination of above

### Pagination

Use `limit` and `skip` parameters:

```bash
# Get next 20 transactions
curl "http://localhost:3003/transactions/?limit=20&skip=20" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Category Summary

Get aggregated totals by category:

```bash
curl "http://localhost:3003/transactions/summary/by-category?start_date=2026-02-01&end_date=2026-02-28&type=expense" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Integration with Other Services

- **Auth Service:** Validates JWT tokens
- **Budget Service:** Provides category structure
- **Analytics Service:** Uses transaction data for calculations and trends

## Troubleshooting

**MongoDB connection errors:**

- Ensure MongoDB is running: `mongod --version`
- Check `MONGO_URI` in `.env`
- Verify network connectivity

**JWT validation errors:**

- Ensure `JWT_SECRET` matches Auth Service
- Check token is included in Authorization header
- Verify token hasn't expired

**Import errors:**

- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Development

**Run in debug mode:**

```bash
export NODE_ENV=development  # Linux/macOS
set NODE_ENV=development     # Windows
python app.py
```

**Check service health:**

```bash
curl http://localhost:3003/health
```

## License

MIT
