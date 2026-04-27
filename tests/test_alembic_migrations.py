"""
Integration tests for Alembic migrations.
Requires DATABASE_URL to be set in the environment or .env file.
"""
import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from alembic.config import Config
from alembic import command

load_dotenv()


@pytest.fixture(scope="module")
def engine():
    url = os.environ["DATABASE_URL"]
    return create_engine(url)


@pytest.fixture(scope="module", autouse=True)
def run_migrations(engine):
    cfg = Config("alembic/alembic.ini")
    cfg.set_main_option("sqlalchemy.url", str(engine.url))
    command.upgrade(cfg, "head")
    yield
    command.downgrade(cfg, "base")


def test_users_table_exists(engine):
    inspector = inspect(engine)
    assert "users" in inspector.get_table_names()


def test_users_columns(engine):
    inspector = inspect(engine)
    cols = {c["name"] for c in inspector.get_columns("users")}
    assert {"id", "username", "email", "created_at"}.issubset(cols)


def test_email_index_exists(engine):
    inspector = inspect(engine)
    indexes = {idx["name"] for idx in inspector.get_indexes("users")}
    assert "ix_users_email" in indexes


def test_posts_table_exists(engine):
    inspector = inspect(engine)
    assert "posts" in inspector.get_table_names()


def test_posts_foreign_key(engine):
    inspector = inspect(engine)
    fks = inspector.get_foreign_keys("posts")
    assert any(fk["referred_table"] == "users" for fk in fks)


def test_insert_and_query(engine):
    with engine.begin() as conn:
        conn.execute(text(
            "INSERT INTO users (username, email) VALUES (:u, :e) ON CONFLICT DO NOTHING"
        ), {"u": "test_user", "e": "test@example.com"})
        result = conn.execute(text("SELECT username FROM users WHERE username = 'test_user'"))
        assert result.fetchone() is not None
