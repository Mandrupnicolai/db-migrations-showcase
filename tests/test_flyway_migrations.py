"""
Integration tests for Flyway migrations.
Requires POSTGRES_* env vars set in the environment or .env file.
Flyway CLI must be on PATH.
"""
import os
import subprocess
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv()


@pytest.fixture(scope="module")
def engine():
    url = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )
    return create_engine(url)


@pytest.fixture(scope="module", autouse=True)
def run_flyway(engine):
    flyway_url = (
        f"jdbc:postgresql://{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}"
        f"/{os.environ['POSTGRES_DB']}"
    )
    env = {
        **os.environ,
        "FLYWAY_URL": flyway_url,
        "FLYWAY_USER": os.environ["POSTGRES_USER"],
        "FLYWAY_PASSWORD": os.environ["POSTGRES_PASSWORD"],
    }
    subprocess.run(
        ["flyway", "-configFiles=conf/flyway.toml", "migrate"],
        cwd="flyway",
        env=env,
        check=True,
    )
    yield


def test_flyway_users_table(engine):
    inspector = inspect(engine)
    assert "users" in inspector.get_table_names()


def test_flyway_posts_table(engine):
    inspector = inspect(engine)
    assert "posts" in inspector.get_table_names()


def test_flyway_schema_history(engine):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM flyway_schema_history"))
        count = result.scalar()
        assert count >= 3
