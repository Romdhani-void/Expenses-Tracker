@echo off
echo Setting up PostgreSQL databases for Expense Tracker...
echo.

REM Set PostgreSQL password
set PGPASSWORD=root

echo Creating databases if they don't exist...
psql -U postgres -c "CREATE DATABASE expense_tracker_auth;" 2>nul
psql -U postgres -c "CREATE DATABASE expense_tracker_budget;" 2>nul

echo.
echo Running schema for Auth Service...
psql -U postgres -d expense_tracker_auth -f auth-service\docs\schema.sql

echo.
echo Running schema for Budget Service...
psql -U postgres -d expense_tracker_budget -f budget-service\docs\schema.sql

echo.
echo Database setup complete!
echo.
pause