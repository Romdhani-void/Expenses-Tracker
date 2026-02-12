const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

async function setupDatabase(dbName, schemaPath, description) {
  console.log(`\n📦 Setting up ${description}...`);
  
  const pool = new Pool({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'root',
    database: dbName
  });

  try {
    // Read schema file
    const schema = fs.readFileSync(schemaPath, 'utf8');
    
    // Execute schema
    await pool.query(schema);
    
    console.log(`✓ ${description} tables created successfully`);
    
    // Verify tables
    const result = await pool.query(`
      SELECT tablename FROM pg_tables 
      WHERE schemaname = 'public'
      ORDER BY tablename
    `);
    
    console.log(`  Tables: ${result.rows.map(r => r.tablename).join(', ')}`);
    
  } catch (error) {
    console.error(`✗ Error setting up ${description}:`, error.message);
  } finally {
    await pool.end();
  }
}

async function createDatabaseIfNeeded(dbName) {
  const pool = new Pool({
    host: 'localhost',
    port: 5432,
    user: 'postgres',
    password: 'root',
    database: 'postgres'
  });

  try {
    const result = await pool.query(
      "SELECT 1 FROM pg_database WHERE datname = $1",
      [dbName]
    );

    if (result.rows.length === 0) {
      await pool.query(`CREATE DATABASE ${dbName}`);
      console.log(`✓ Created database: ${dbName}`);
    } else {
      console.log(`✓ Database exists: ${dbName}`);
    }
  } catch (error) {
    console.error(`✗ Error checking/creating database ${dbName}:`, error.message);
  } finally {
    await pool.end();
  }
}

async function main() {
  console.log('='.repeat(60));
  console.log('🚀 Expense Tracker - Database Setup');
  console.log('='.repeat(60));

  try {
    // Ensure databases exist
    console.log('\n📋 Step 1: Checking databases...');
    await createDatabaseIfNeeded('expense_tracker_auth');
    await createDatabaseIfNeeded('expense_tracker_budget');

    // Setup auth service database
    console.log('\n📋 Step 2: Creating tables...');
    await setupDatabase(
      'expense_tracker_auth',
      path.join(__dirname, 'auth-service', 'docs', 'schema.sql'),
      'Auth Service'
    );

    // Setup budget service database
    await setupDatabase(
      'expense_tracker_budget',
      path.join(__dirname, 'budget-service', 'docs', 'schema.sql'),
      'Budget Service'
    );

    console.log('\n' + '='.repeat(60));
    console.log('✅ Database setup complete!');
    console.log('='.repeat(60));
    console.log('\n💡 You can now restart your backend services:\n   npm run go\n');

  } catch (error) {
    console.error('\n❌ Setup failed:', error.message);
    console.log('\nMake sure:');
    console.log('  1. PostgreSQL is running');
    console.log('  2. Username: postgres, Password: root');
    console.log('  3. PostgreSQL is accessible on localhost:5432');
  }
}

main();
