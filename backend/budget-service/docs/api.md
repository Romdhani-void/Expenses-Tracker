# Budget Service API Documentation

Base URL: `http://localhost:3002`

All endpoints require JWT authentication via `Authorization: Bearer {token}` header.

## Budget Endpoints

### 1. Get All Budgets

**GET** `/budgets`

Retrieve all budgets for the authenticated user.

**Headers:**

```
Authorization: Bearer {token}
```

**Response (200 OK):**

```json
{
  "budgets": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "year": 2026,
      "month": 2,
      "currency": "USD",
      "opening_balance": 5000.0,
      "closing_balance": 4500.0,
      "category_count": 8,
      "created_at": "2026-02-01T00:00:00Z",
      "updated_at": "2026-02-11T12:13:18Z"
    }
  ]
}
```

---

### 2. Get Specific Budget

**GET** `/budgets/:id`

Get a specific budget with its categories.

**Response (200 OK):**

```json
{
  "budget": {
    "id": "uuid",
    "user_id": "uuid",
    "year": 2026,
    "month": 2,
    "currency": "USD",
    "opening_balance": 5000.0,
    "closing_balance": 4500.0,
    "created_at": "2026-02-01T00:00:00Z",
    "categories": [
      {
        "id": "uuid",
        "budget_id": "uuid",
        "name": "Rent",
        "planned_amount": 1200.0,
        "actual_amount": 1200.0,
        "currency": "USD",
        "is_recurring": true,
        "recurring_amount": 1200.0
      }
    ]
  }
}
```

---

### 3. Get Budget by Month/Year

**GET** `/budgets/month/:year/:month`

Get budget for a specific month.

**Example:** `GET /budgets/month/2026/2`

**Response:** Same as Get Specific Budget

---

### 4. Create Budget

**POST** `/budgets`

Create a new monthly budget.

**Request Body:**

```json
{
  "year": 2026,
  "month": 3,
  "currency": "CAD",
  "opening_balance": 6000.0
}
```

**Response (201 Created):**

```json
{
  "message": "Budget created successfully",
  "budget": {
    "id": "uuid",
    "user_id": "uuid",
    "year": 2026,
    "month": 3,
    "currency": "CAD",
    "opening_balance": 6000.0,
    "closing_balance": 6000.0,
    "created_at": "2026-03-01T00:00:00Z"
  }
}
```

**Error Responses:**

- `400`: Missing required fields
- `409`: Budget already exists for this month

---

### 5. Update Budget

**PUT** `/budgets/:id`

Update budget balances or currency.

**Request Body:**

```json
{
  "opening_balance": 5500.0,
  "closing_balance": 4200.0,
  "currency": "USD"
}
```

**Response (200 OK):**

```json
{
  "message": "Budget updated successfully",
  "budget": { ... }
}
```

---

### 6. Delete Budget

**DELETE** `/budgets/:id`

Delete a budget and all its categories.

**Response (200 OK):**

```json
{
  "message": "Budget deleted successfully"
}
```

---

## Category Endpoints

### 1. Get All Categories for Budget

**GET** `/categories/budget/:budgetId`

Get all categories for a specific budget.

**Response (200 OK):**

```json
{
  "categories": [
    {
      "id": "uuid",
      "budget_id": "uuid",
      "name": "Groceries",
      "planned_amount": 400.0,
      "actual_amount": 385.5,
      "currency": "USD",
      "is_recurring": true,
      "recurring_amount": 400.0,
      "created_at": "2026-02-01T00:00:00Z"
    }
  ]
}
```

---

### 2. Create Category

**POST** `/categories`

Create a new budget category.

**Request Body:**

```json
{
  "budget_id": "uuid",
  "name": "Entertainment",
  "planned_amount": 200.0,
  "currency": "USD",
  "is_recurring": true,
  "recurring_amount": 200.0
}
```

**Response (201 Created):**

```json
{
  "message": "Category created successfully",
  "category": { ... }
}
```

**Error Responses:**

- `400`: Missing required fields
- `404`: Budget not found
- `409`: Category with this name already exists

---

### 3. Update Category

**PUT** `/categories/:id`

Update category amounts or settings.

**Request Body:**

```json
{
  "planned_amount": 250.0,
  "actual_amount": 180.0,
  "is_recurring": true,
  "recurring_amount": 250.0
}
```

**Response (200 OK):**

```json
{
  "message": "Category updated successfully",
  "category": { ... }
}
```

---

### 4. Delete Category

**DELETE** `/categories/:id`

Delete a category.

**Response (200 OK):**

```json
{
  "message": "Category deleted successfully"
}
```

---

### 5. Bulk Create Categories

**POST** `/categories/bulk`

Create multiple categories at once (useful for recurring categories).

**Request Body:**

```json
{
  "budget_id": "uuid",
  "categories": [
    {
      "name": "Rent",
      "currency": "USD",
      "is_recurring": true,
      "recurring_amount": 1200.0
    },
    {
      "name": "Utilities",
      "currency": "USD",
      "is_recurring": true,
      "recurring_amount": 150.0
    }
  ]
}
```

**Response (201 Created):**

```json
{
  "message": "2 categories created successfully",
  "categories": [ ... ]
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
  "service": "budget-service"
}
```

---

## Multi-Currency Support

Budgets and categories support multiple currencies. Common currencies:

- `USD` - US Dollar
- `CAD` - Canadian Dollar
- `HUF` - Hungarian Forint
- `EUR` - Euro
- `GBP` - British Pound

**Note:** Exchange rate conversion is handled by the Analytics Service.

---

## Recurring Categories

Categories can be marked as recurring with a `recurring_amount`:

```json
{
  "name": "Rent",
  "is_recurring": true,
  "recurring_amount": 1200.0
}
```

This allows auto-filling planned amounts when creating budgets for subsequent months.

---

## Error Handling

All errors follow this format:

```json
{
  "error": "Error message"
}
```

Common HTTP status codes:

- `400`: Bad Request
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden
- `404`: Resource not found
- `409`: Conflict
- `500`: Internal Server Error
