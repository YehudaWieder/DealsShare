import sqlite3
from config import DB_PATH

DB_PATH = DB_PATH

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT CHECK(gender IN ('male','female','other')),
                password BLOB NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_email TEXT NOT NULL,
                name TEXT NOT NULL,
                features TEXT,
                free_shipping INTEGER DEFAULT 0,
                description TEXT,
                category TEXT,
                regular_price REAL,
                discount_price REAL,
                image_url TEXT,
                link TEXT,
                publish_date TEXT,
                FOREIGN KEY (seller_email) REFERENCES users(email) ON DELETE CASCADE
            )
        """)

        
        # Ratings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                seller_email TEXT NOT NULL,
                product_id INTEGER,
                rating INTEGER CHECK(rating BETWEEN 1 AND 5),
                FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE SET NULL,
                FOREIGN KEY (seller_email) REFERENCES users(email) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
            )
        """)

        
        # Favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_email TEXT NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (user_email, product_id),
                FOREIGN KEY (user_email) REFERENCES users(email) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)


        conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")