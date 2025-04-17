import asyncio
from pathlib import Path

import asyncpg
from loguru import logger


async def seed_database():
    # Database connection parameters
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASSWORD = "mysecretpassword"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        # Create connection
        conn = await asyncpg.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        logger.info("Connected to database successfully")

        # Read SQL file
        sql_file_path = Path(__file__).parent / "seed_data.sql"
        with open(sql_file_path, "r") as file:
            sql_content = file.read()

        # Execute SQL commands
        logger.info("Starting database seeding...")

        # Split the SQL content into individual statements
        # This handles multiple statements separated by semicolons
        statements = sql_content.split(";")

        # Execute each statement
        for statement in statements:
            # Skip empty statements
            if statement.strip():
                try:
                    await conn.execute(statement)
                except Exception as e:
                    logger.error(f"Error executing statement: {e}")
                    logger.debug(f"Failed statement: {statement}")
                    raise

        logger.success("Database seeded successfully!")

    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        raise

    finally:
        # Close connection
        if "conn" in locals():
            await conn.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    try:
        asyncio.run(seed_database())
    except KeyboardInterrupt:
        logger.warning("Seeding interrupted by user")
    except Exception as e:
        logger.error(f"Seeding failed: {e}")
        exit(1)
