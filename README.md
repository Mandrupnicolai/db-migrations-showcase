# db-migrations-showcase

> A professional side-by-side comparison of **Alembic** (Python) and **Flyway** (Java/SQL) database migration tools against **PostgreSQL** — with integration tests and dual CI/CD pipelines.

[![Alembic CI](https://github.com/Mandrupnicolai/db-migrations-showcase/actions/workflows/alembic.yml/badge.svg)](https://github.com/Mandrupnicolai/db-migrations-showcase/actions/workflows/alembic.yml)
[![Flyway CI](https://github.com/Mandrupnicolai/db-migrations-showcase/actions/workflows/flyway.yml/badge.svg)](https://github.com/Mandrupnicolai/db-migrations-showcase/actions/workflows/flyway.yml)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![PostgreSQL](https://img.shields.io/badge/postgres-16-336791?logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Why this project exists

Schema management is one of the most error-prone parts of production engineering. This repo demonstrates how to approach it properly — versioned, repeatable, reversible, and automated — using two of the most widely adopted tools in the ecosystem.

---
## Project Structure

```
db-migrations-showcase/
├── alembic/
│   ├── versions/        # Versioned migration files
│   ├── env.py           # Alembic runtime environment
│   └── alembic.ini      # Configuration (no hardcoded credentials)
├── flyway/
│   ├── conf/            # Flyway config (env-var driven)
│   └── sql/             # V1, V2, V3 SQL migration scripts
├── docker/              # Local Postgres via Docker Compose
├── scripts/             # PowerShell helper scripts
├── tests/               # Integration tests (pytest)
├── .github/
│   └── workflows/       # GitHub Actions pipelines
└── .gitlab-ci.yml       # GitLab CI pipeline
```

## Prerequisites

| Tool       | Version |
|------------|---------|
| Python     | 3.11+   |
| Java       | 17+     |
| Flyway CLI | 10+     |
| Docker     | 24+     |
| PowerShell | 7+      |

---

## Quick Start

### 1. Clone & configure

```bash
git clone https://github.com/Mandrupnicolai/db-migrations-showcase.git
cd db-migrations-showcase
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start the database

```bash
docker compose -f docker/docker-compose.yml up -d
```

### 3. Run Alembic migrations

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
.\scripts\run_alembic.ps1
```

### 4. Run Flyway migrations

```powershell
.\scripts\run_flyway.ps1
```

### 5. Run the test suite

```bash
pytest tests/ -v
```

---

## CI/CD Pipelines

Both **GitHub Actions** and **GitLab CI** pipelines run automatically on every push and pull request.

### What each pipeline does

| Step | Alembic | Flyway |
|------|---------|--------|
| Spin up Postgres service container | ✅ | ✅ |
| Run full migration chain to `head` | ✅ | ✅ |
| Downgrade to `base` (rollback smoke test) | ✅ | — |
| Upgrade to `head` again (idempotency check) | ✅ | — |
| Validate with `flyway info` | — | ✅ |
| Run integration tests (pytest) | ✅ | ✅ |

### Secrets required

Add these in **Settings → Secrets and variables → Actions** (GitHub) or **Settings → CI/CD → Variables** (GitLab):

| Secret | Description |
|--------|-------------|
| `POSTGRES_DB` | Database name |
| `POSTGRES_USER` | Database user |
| `POSTGRES_PASSWORD` | Database password |

---

## Tool Comparison

| Feature | Alembic | Flyway |
|---------|---------|--------|
| Language | Python | Any (SQL-first) |
| Schema definition | SQLAlchemy ORM or raw SQL | Pure SQL |
| Rollback support | Yes (`downgrade()`) | Flyway Teams+ |
| Auto-generation | Yes (`autogenerate`) | No |
| Version format | Free-form rev IDs | `Vx__description.sql` |
| Best for | Python stacks | Polyglot / Java stacks |

---

## Key Concepts Demonstrated

- **Versioned migrations** — every schema change is tracked, ordered, and auditable
- **Reversible migrations** — downgrade paths enable safe rollbacks in production
- **Environment-based config** — zero hardcoded credentials anywhere in the codebase
- **Idempotency testing** — up → down → up cycle proves migration correctness
- **CI gate** — all migrations and tests must pass before a branch can merge

---

## License

MIT
