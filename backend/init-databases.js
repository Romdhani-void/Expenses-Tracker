const { Client } = require('pg');
const fs = require('fs');
const path = require('path');

// Database connection parameters
const DB_HOST = 'localhost';
const DB_PORT = 5432;
const DB_USER = 'postgres';
const DB_PASSWORD = 'root';

// Read schema files
const authSchema = fs.readFileSync(
  path.join(__dirname, 'auth-service', 'docs', 'schema.sql'),
  'utf8'
);

const budgetSchema = fs.readFileSync(
  path.join(__dirname, 'budget-service', 'docs', 'schema.sql'),
  'utf8'
);

async function createDatabaseIfNotExists(dbName) {
  const client = new Client({
    host: DB_HOST,
    port: DB_PORT,
    user: DB_USER,
    password: DB_PASSWORD,
    database: 'postgres'
  });

  try {
    await client.connect();
    
    // Check if database exists
    const result = await client.query(
      "SELECT 1 FROM pg_database WHERE datname = $1",
      [dbName]
    );

    if (result.rows.length === 0) {
      await client.query(`CREATE DATABASE ${dbName}`);
      console.log(`✓ Created database: ${dbName}`);
    } else {
      console.log(`✓ Database already exists: ${dbName}`);
    }
  } catch (error) {
    console.error(`✗ Error creating database ${dbName}:`, error.message);
  } finally {
    await client.end();
  }
}

async function runSchema(dbName, schemaSql) {
  const client = new Client({
    host: DB_HOST,
    port: DB_PORT,
    user: DB_USER,
    password: DB_PASSWORD,
    database: dbName
  });

  try {
    await client.connect();
    await client.query(schemaSql);
    console.log(`✓ Schema applied successfully to ${dbName}`);
  } catch (error) {
    console.error(`✗ Error applying schema to ${dbName}:`, error.message);
  } finally {
    await client.end();
  }
}

async function main() {
  console.log('='.repeat(60));
  console.log('Expense Tracker - Database Initialization Script');
  console.log('='.repeat(60));
  console.log();

  try {
    console.log('Step 1: Creating databases...');
    await createDatabaseIfNotExists('expense_tracker_auth');
    await createDatabaseIfNotExists('expense_tracker_budget');
    console.log();

    console.log('Step 2: Applying schemas...');
    await runSchema('expense_tracker_auth', authSchema);
    await runSchema('expense_tracker_budget', budgetSchema);
    console.log();

    console.log('='.repeat(60));
    console.log('✓ Database initialization complete!');
    console.log('='.repeat(60));
    console.log();
    console.log('You can now restart your backend services.');
  } catch (error) {
    console.error('✗ Error:', error.message);
    console.log('\nMake sure PostgreSQL is running and credentials are correct.');
  }
}

main();
