-- Budget Service PostgreSQL schema

-- Budgets table - stores monthly budgets
CREATE TABLE IF NOT EXISTS budgets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
  currency VARCHAR(3) NOT NULL DEFAULT 'USD',
  opening_balance DECIMAL(15, 2) DEFAULT 0,
  closing_balance DECIMAL(15, 2) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, year, month)
);

-- Budget categories table - stores spending limits per category
CREATE TABLE IF NOT EXISTS budget_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  budget_id UUID NOT NULL REFERENCES budgets(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  planned_amount DECIMAL(15, 2) DEFAULT 0,
  actual_amount DECIMAL(15, 2) DEFAULT 0,
  currency VARCHAR(3) NOT NULL DEFAULT 'USD',
  is_recurring BOOLEAN DEFAULT FALSE,
  recurring_amount DECIMAL(15, 2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(budget_id, name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_budgets_user_id ON budgets(user_id);
CREATE INDEX IF NOT EXISTS idx_budgets_year_month ON budgets(year, month);
CREATE INDEX IF NOT EXISTS idx_budget_categories_budget_id ON budget_categories(budget_id);
