# Analytics Service

## Endpoints

Base URL: `http://localhost:3004`

All endpoints require JWT authentication.

### 1. Get Monthly Summary

**GET** `/analytics/month/{year}/{month}`

Returns complete monthly analytics including income, expenses, closing balance, and budget comparison.

### 2. Get Category Summary

**GET** `/analytics/categories?start_date={date}&end_date={date}`

Returns spending breakdown by category.

### 3. Get Budget vs Actual

**GET** `/analytics/budget-vs-actual/{year}/{month}`

Compares planned budget vs actual spending per category.

### 4. Get Real Available Money

**GET** `/analytics/real-available/{year}/{month}?saves={amount}`

Calculates real available money (closing balance - designated saves).

See full documentation in docs/api.md
