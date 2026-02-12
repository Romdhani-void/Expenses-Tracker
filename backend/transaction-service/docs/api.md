# Transaction Service API Documentation

Base URL: `http://localhost:3003`

All endpoints require JWT authentication via `Authorization: Bearer {token}` header.

## Transaction Endpoints

### 1. Get All Transactions

**GET** `/transactions/`

Retrieve transactions with optional filtering.

**Headers:**

```
Authorization: Bearer {token}
```

**Query Parameters:**

- `type` (optional): Filter by type ("income" or "expense")
- `category` (optional): Filter by category name
- `start_date` (optional): Filter from date (ISO format: YYYY-MM-DD)
- `end_date` (optional): Filter to date (ISO format: YYYY-MM-DD)
- `limit` (optional): Number of results (default: 100)
- `skip` (optional): Number to skip for pagination (default: 0)

**Response (200 OK):**

```json
{
  "transactions": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "user_id": "user-uuid",
      "type": "expense",
      "amount": 45.5,
      "currency": "USD",
      "category": "Groceries",
      "date": "2026-02-10T14:30:00Z",
      "notes": "Weekly shopping",
      "created_at": "2026-02-10T14:35:00Z",
      "updated_at": "2026-02-10T14:35:00Z"
    }
  ],
  "total": 150,
  "limit": 100,
  "skip": 0
}
```

---

### 2. Get Transaction by ID

**GET** `/transactions/<transaction_id>`

Get a specific transaction.

**Response (200 OK):**

```json
{
  "transaction": {
    "_id": "507f1f77bcf86cd799439011",
    "user_id": "user-uuid",
    "type": "income",
    "amount": 3500.0,
    "currency": "USD",
    "category": "Salary",
    "date": "2026-02-01T00:00:00Z",
    "notes": "Monthly salary",
    "created_at": "2026-02-01T08:00:00Z",
    "updated_at": "2026-02-01T08:00:00Z"
  }
}
```

**Error:**

- `404`: Transaction not found

---

### 3. Create Transaction

**POST** `/transactions/`

Create a new transaction (income or expense).

**Request Body:**

```json
{
  "type": "expense",
  "amount": 127.0,
  "currency": "HUF",
  "category": "Rent",
  "date": "2026-02-05T10:00:00Z",
  "notes": "Monthly rent payment"
}
```

**Required Fields:**

- `type`: "income" or "expense"
- `amount`: Positive number
- `currency`: 3-letter code (USD, CAD, HUF, etc.)
- `category`: Category name
- `date`: ISO 8601 date string

**Optional Fields:**

- `notes`: Additional description

**Response (201 Created):**

```json
{
  "message": "Transaction created successfully",
  "transaction": { ... }
}
```

**Error Responses:**

- `400`: Validation error (missing fields, invalid format)

---

### 4. Update Transaction

**PUT** `/transactions/<transaction_id>`

Update an existing transaction.

**Request Body (all fields optional):**

```json
{
  "amount": 130.0,
  "category": "Rent",
  "notes": "Updated rent amount"
}
```

**Response (200 OK):**

```json
{
  "message": "Transaction updated successfully",
  "transaction": { ... }
}
```

**Error:**

- `404`: Transaction not found

---

### 5. Delete Transaction

**DELETE** `/transactions/<transaction_id>`

Delete a transaction.

**Response (200 OK):**

```json
{
  "message": "Transaction deleted successfully"
}
```

**Error:**

- `404`: Transaction not found

---

### 6. Get Summary by Category

**GET** `/transactions/summary/by-category`

Get aggregated totals by category.

**Query Parameters:**

- `start_date` (optional): Filter from date
- `end_date` (optional): Filter to date
- `type` (optional): Filter by type ("income" or "expense")

**Response (200 OK):**

```json
{
  "summary": [
    {
      "category": "Groceries",
      "total": 385.5,
      "count": 12,
      "currency": "USD"
    },
    {
      "category": "Rent",
      "total": 1200.0,
      "count": 1,
      "currency": "USD"
    }
  ]
}
```

---

## Health Check

### GET `/health`

Check if service is running (no authentication required).

**Response (200 OK):**

```json
{
  "status": "ok",
  "service": "transaction-service"
}
```

---

## Usage Examples

### Add Income

```bash
curl -X POST http://localhost:3003/transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "income",
    "amount": 3500,
    "currency": "USD",
    "category": "Salary",
    "date": "2026-02-01T00:00:00Z",
    "notes": "Monthly salary"
  }'
```

### Add Expense

```bash
curl -X POST http://localhost:3003/transactions/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "expense",
    "amount": 45.50,
    "currency": "USD",
    "category": "Groceries",
    "date": "2026-02-10T14:30:00Z",
    "notes": "Weekly shopping"
  }'
```

### Filter Transactions

```bash
# Get all expenses in February 2026
curl -X GET "http://localhost:3003/transactions/?type=expense&start_date=2026-02-01&end_date=2026-02-28" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get all transactions in Groceries category
curl -X GET "http://localhost:3003/transactions/?category=Groceries" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Category Summary

```bash
curl -X GET "http://localhost:3003/transactions/summary/by-category?start_date=2026-02-01&end_date=2026-02-28&type=expense" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Error Handling

All errors follow this format:

```json
{
  "error": "Error description"
}
```

Common HTTP status codes:

- `400`: Bad Request (validation errors)
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

---

## Data Types

### Transaction Types

- `income`: Money received (salary, extra income, etc.)
- `expense`: Money spent (purchases, bills, etc.)

### Common Categories

**Income:**

- Salary
- Extra Income
- Freelance
- Bonuses

**Expenses:**

- Rent
- Utilities
- Groceries
- Transportation
- Entertainment
- Healthcare
- Insurance

### Currencies

Use ISO 4217 3-letter currency codes:

- USD - US Dollar
- CAD - Canadian Dollar
- HUF - Hungarian Forint
- EUR - Euro
- GBP - British Pound
