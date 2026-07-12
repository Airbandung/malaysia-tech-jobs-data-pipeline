import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection() -> psycopg2.extensions.connection:
    """
    Establishes a connection to the PostgreSQL database using environment variables.

    Returns:
        connection: A psycopg2 connection object to the PostgreSQL database.
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return connection
    except Exception as e:
        raise Exception(f"Error connecting to the database: {e}")
    
    