import sqlite3
from config import DB_PATH

DB_PATH = DB_PATH

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password BLOB NOT NULL,
                role TEXT NOT NULL
            )
        """)
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                image_url TEXT,
                regular_price REAL,
                discount_price REAL,
                deal_expiry TEXT,
                link TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")