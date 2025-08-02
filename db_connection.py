import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
   
    conn = psycopg2.connect(database_url)
    return conn

def test_connection():
    """Test the database connection"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print("Database connection successful!")
        print(f"Test query result: {result}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
