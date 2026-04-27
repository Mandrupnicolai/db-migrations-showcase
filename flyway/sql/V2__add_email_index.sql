-- V2: Add unique index on email
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
