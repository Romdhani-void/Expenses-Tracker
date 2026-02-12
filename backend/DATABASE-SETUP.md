# Database Setup (Docker Images)

Use **Docker images** to run PostgreSQL, MongoDB, and Redis. No local installation required. Run each container once; your app connects to `localhost` with the ports below.

All commands assume you are in the project root: `Expense Tracker`.

---

## 1. PostgreSQL (Auth + Budget services)

One container; two databases inside it.

**Run the container:**

```bash
docker run -d --name expense-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:16
```

**Create databases:**

```bash
docker exec expense-postgres psql -U postgres -c "CREATE DATABASE expense_tracker_auth;"
docker exec expense-postgres psql -U postgres -c "CREATE DATABASE expense_tracker_budget;"
```

**Apply schemas** (from project root):

```bash
docker cp backend/auth-service/docs/schema.sql expense-postgres:/tmp/auth_schema.sql
docker cp backend/budget-service/docs/schema.sql expense-postgres:/tmp/budget_schema.sql

docker exec expense-postgres psql -U postgres -d expense_tracker_auth -f /tmp/auth_schema.sql
docker exec expense-postgres psql -U postgres -d expense_tracker_budget -f /tmp/budget_schema.sql
```

**Connection (for .env):** `DB_HOST=localhost`, `DB_PORT=5432`, `DB_NAME=expense_tracker_auth` or `expense_tracker_budget`, `DB_USER=postgres`, `DB_PASSWORD=password`.

---

## 2. MongoDB (Transaction service)

**Run the container:**

```bash
docker run -d --name expense-mongo -p 27017:27017 mongo:7
```

The app creates the database and collections on first use.

**Connection (for .env):** `MONGO_URI=mongodb://localhost:27017/`, `MONGO_DB_NAME=expense_tracker_transactions`.

---

## 3. Redis (Analytics service cache)

**Run the container:**

```bash
docker run -d --name expense-redis -p 6379:6379 redis:7
```

**Connection (for .env):** `REDIS_HOST=localhost`, `REDIS_PORT=6379`, `REDIS_DB=0`. Analytics runs without Redis if the container is not running (no cache).

---

## 4. RabbitMQ (optional – async between services)

Only if you add message-based features later.

```bash
docker run -d --name expense-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

No app configuration required for the base setup.

---

## Summary: ports and .env

| Store    | Container port (host) | Used by           |
|----------|------------------------|-------------------|
| Postgres | 5432                   | Auth, Budget      |
| MongoDB  | 27017                  | Transaction       |
| Redis    | 6379                   | Analytics (cache) |

Copy each service’s `.env.example` to `.env` and set the values above so the app connects to these Docker-backed databases.

---

## Useful commands

- List running DB containers: `docker ps --filter "name=expense-"`
- Stop: `docker stop expense-postgres expense-mongo expense-redis`
- Start again: `docker start expense-postgres expense-mongo expense-redis`
- Remove (data lost): `docker rm -f expense-postgres expense-mongo expense-redis`

If you use **locally installed** PostgreSQL instead of Docker, you can run `backend/setup-databases.bat` (Windows) or the equivalent `psql` commands from this doc using your local Postgres. The app still connects via the same `.env` values (e.g. `DB_HOST=localhost`, `DB_PORT=5432`).
