-- Create game_store schema if it doesn't exist
BEGIN
IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'game_store') THEN
CREATE SCHEMA game_store;
RAISE NOTICE 'Created schema game_store';
ELSE
RAISE NOTICE 'Schema game_store already exists';
END IF;
END;
