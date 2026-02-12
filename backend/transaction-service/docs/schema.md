# MongoDB Schema Documentation

## Database: expense_tracker_transactions

MongoDB is a NoSQL database, so schemas are flexible. However, the transaction documents follow this structure:

## Collection: transactions

### Document Schema

```json
{
  "_id": ObjectId,
  "user_id": "UUID string (from auth service)",
  "type": "income" | "expense",
  "amount": Number (Decimal),
  "currency": "String (3-letter code, e.g., USD, CAD, HUF)",
  "category": "String (e.g., Salary, Groceries, Rent)",
  "date": "ISO 8601 date string (e.g., 2026-02-11T12:00:00Z)",
  "notes": "String (optional)",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp"
}
```

### Field Descriptions

| Field      | Type          | Required | Description                                         |
| ---------- | ------------- | -------- | --------------------------------------------------- |
| \_id       | ObjectId      | Auto     | MongoDB document ID                                 |
| user_id    | String (UUID) | Yes      | ID of the user who owns this transaction            |
| type       | String        | Yes      | Transaction type: "income" or "expense"             |
| amount     | Number        | Yes      | Transaction amount (must be > 0)                    |
| currency   | String        | Yes      | 3-letter currency code (USD, CAD, HUF, etc.)        |
| category   | String        | Yes      | Category name (e.g., "Salary", "Groceries", "Rent") |
| date       | String (ISO)  | Yes      | Transaction date in ISO 8601 format                 |
| notes      | String        | No       | Optional notes or description                       |
| created_at | String (ISO)  | Auto     | When the transaction was created                    |
| updated_at | String (ISO)  | Auto     | When the transaction was last updated               |

### Indexes

For optimal query performance, the following indexes are created:

1. **user_id (ascending)** - For filtering by user
2. **date (descending)** - For date-based queries and sorting
3. **category (ascending)** - For category filtering
4. **type (ascending)** - For filtering income vs expenses
5. **Compound index (user_id + date)** - For user-specific date queries

### Example Documents

**Income Transaction:**

```json
{
  "_id": "ObjectId('507f1f77bcf86cd799439011')",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "income",
  "amount": 3500.0,
  "currency": "USD",
  "category": "Salary",
  "date": "2026-02-01T00:00:00Z",
  "notes": "Monthly salary",
  "created_at": "2026-02-01T08:30:00Z",
  "updated_at": "2026-02-01T08:30:00Z"
}
```

**Expense Transaction:**

```json
{
  "_id": "ObjectId('507f1f77bcf86cd799439012')",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "type": "expense",
  "amount": 127.0,
  "currency": "HUF",
  "category": "Rent",
  "date": "2026-02-05T10:00:00Z",
  "notes": "Monthly rent payment",
  "created_at": "2026-02-05T10:15:00Z",
  "updated_at": "2026-02-05T10:15:00Z"
}
```

### Query Examples

**Find all transactions for a user:**

```javascript
db.transactions.find({ user_id: "user-uuid" });
```

**Find expenses in a date range:**

```javascript
db.transactions.find({
  user_id: "user-uuid",
  type: "expense",
  date: {
    $gte: "2026-02-01",
    $lte: "2026-02-28",
  },
});
```

**Find transactions by category:**

```javascript
db.transactions.find({
  user_id: "user-uuid",
  category: "Groceries",
});
```

**Aggregate total expenses by category:**

```javascript
db.transactions.aggregate([
  { $match: { user_id: "user-uuid", type: "expense" } },
  {
    $group: {
      _id: "$category",
      total: { $sum: "$amount" },
      count: { $sum: 1 },
    },
  },
  { $sort: { total: -1 } },
]);
```

### Data Validation

The application enforces these validation rules:

- `type` must be either "income" or "expense"
- `amount` must be a positive number
- `currency` must be a 3-letter code
- `date` must be a valid ISO 8601 date string
- `user_id`, `type`, `amount`, `currency`, `category`, and `date` are required

### Setup

To set up the MongoDB database:

```bash
# Start MongoDB
mongod

# Create database (happens automatically on first insert)
# Connect to MongoDB shell
mongosh

# Switch to database
use expense_tracker_transactions

# The indexes and collections will be created automatically
# when the application starts
```
