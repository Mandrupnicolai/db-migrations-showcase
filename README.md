# db-migrations-showcase

> A professional side-by-side comparison of **Alembic** (Python) and **Flyway** (Java/SQL) database migration tools against **PostgreSQL** — with integration tests and dual CI/CD pipelines.

[![Alembic CI](https://github.com/<YOUR_USERNAME>/db-migrations-showcase/actions/workflows/alembic.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/db-migrations-showcase/actions/workflows/alembic.yml)
[![Flyway CI](https://github.com/<YOUR_USERNAME>/db-migrations-showcase/actions/workflows/flyway.yml/badge.svg)](https://github.com/<YOUR_USERNAME>/db-migrations-showcase/actions/workflows/flyway.yml)

---

## Why this project exists

Schema management is one of the most error-prone parts of production engineering. This repo demonstrates how to approach it properly — versioned, repeatable, reversible, and automated — using two of the most widely adopted tools in the ecosystem.

---

## Project Structure

\\\
db-migrations-showcase/
+-- alembic/          # Python/SQLAlchemy migration scripts
+-- flyway/           # SQL-first migration scripts
+-- docker/           # Local Postgres via Docker Compose
+-- scripts/          # PowerShell helper scripts
+-- tests/            # Integration tests (pytest)
+-- .github/          # GitHub Actions pipelines
+-- .gitlab-ci.yml    # GitLab CI pipeline
\\\

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.11+ |
| Java | 17+ |
| Flyway CLI | 10+ |
| Docker | 24+ |
| PowerShell | 7+ |

---

## Quick Start

### 1. Clone & configure

\\\ash
git clone https://github.com/<YOUR_USERNAME>/db-migrations-showcase.git
cd db-migrations-showcase
cp .env.example .env
# Edit .env with your credentials
\\\

### 2. Start the database

\\\ash
docker compose -f docker/docker-compose.yml up -d
\\\

### 3. Run Alembic migrations

\\\powershell
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\run_alembic.ps1
\\\

### 4. Run Flyway migrations

\\\powershell
.\scripts\run_flyway.ps1
\\\

### 5. Run the test suite

\\\ash
pytest tests/ -v
\\\

---

## Tool Comparison

| Feature | Alembic | Flyway |
|---------|---------|--------|
| Language | Python | Any (SQL-first) |
| Schema definition | SQLAlchemy ORM or raw SQL | Pure SQL |
| Rollback support | Yes (downgrade()) | Flyway Teams+ |
| Auto-generation | Yes (autogenerate) | No |
| Version format | Free-form rev IDs | Vx__description.sql |
| Best for | Python stacks | Polyglot / Java stacks |

---

## CI/CD

Both GitHub Actions and GitLab CI pipelines:
- Spin up a fresh Postgres service container
- Run the full migration chain
- Execute the downgrade ? upgrade idempotency check (Alembic)
- Validate with \lyway info\ (Flyway)
- Run integration tests

Secrets required: \POSTGRES_DB\, \POSTGRES_USER\, \POSTGRES_PASSWORD\

---

## Key Concepts Demonstrated

- **Versioned migrations** — every change tracked and ordered
- **Reversible migrations** — downgrade paths for safe rollbacks
- **Environment-based config** — zero hardcoded credentials
- **Idempotency testing** — up ? down ? up proves correctness
- **CI gate** — migrations must pass before merge

---

## License

MIT
