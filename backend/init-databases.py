import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'root'

# SQL schemas
AUTH_SCHEMA = """
-- Auth Service PostgreSQL schema

CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  google_id VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional: sessions table if you want to track active sessions explicitly
CREATE TABLE IF NOT EXISTS sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  jwt_token TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);
"""

BUDGET_SCHEMA = """
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
"""

def create_database_if_not_exists(cursor, db_name):
    """Create database if it doesn't exist"""
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    if not cursor.fetchone():
        cursor.execute(f'CREATE DATABASE {db_name}')
        print(f"✓ Created database: {db_name}")
    else:
        print(f"✓ Database already exists: {db_name}")

def run_schema(db_name, schema_sql):
    """Run schema SQL on specified database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=db_name,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✓ Schema applied successfully to {db_name}")
    except Exception as e:
        print(f"✗ Error applying schema to {db_name}: {e}")

def main():
    print("=" * 60)
    print("Expense Tracker - Database Initialization Script")
    print("=" * 60)
    print()
    
    # Connect to postgres database to create other databases
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database='postgres',
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("Step 1: Creating databases...")
        create_database_if_not_exists(cursor, 'expense_tracker_auth')
        create_database_if_not_exists(cursor, 'expense_tracker_budget')
        
        cursor.close()
        conn.close()
        print()
        
        print("Step 2: Applying schemas...")
        run_schema('expense_tracker_auth', AUTH_SCHEMA)
        run_schema('expense_tracker_budget', BUDGET_SCHEMA)
        print()
        
        print("=" * 60)
        print("✓ Database initialization complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nMake sure PostgreSQL is running and credentials are correct.")

if __name__ == '__main__':
    main()
