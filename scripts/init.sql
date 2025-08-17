-- This script is executed by the official Postgres Docker entrypoint
-- on first initialization when the data directory is empty.

-- Create schema if it doesn't exist (safe to run multiple times).
CREATE SCHEMA IF NOT EXISTS game_store AUTHORIZATION postgres;

-- Optional: document the schema
COMMENT ON SCHEMA game_store IS 'Schema for game store domain';
