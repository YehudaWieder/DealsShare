import sqlite3

DB_PATH = "database/deals.db"


def seed_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Sample users
        users = [
            ("Yehuda", "v4105677@gmail.com", "123456", "admin"),
            ("user", "8449920@gmail.com", "123456", "user"),
            ("user1", "user1@example.com", "123456", "user"),
            ("user2", "user2@example.com", "123456", "user"),
            ("user3", "user3@example.com", "123456", "user"),
            ("user1", "user4@example.com", "123456", "user"),
            ("user2", "user5@example.com", "123456", "user"),
            ("user3", "user6@example.com", "123456", "user")
        ]
        cursor.executemany("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)", users)

        # Sample products
        products = [
            ("1", "Sample Product", "Sample Product", "Sample Product", "/uploads/20250910162033.jpg", 999, 499.99, "2025-09-24", "https://www.duolingo.com/learn"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/example.png", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
            ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
            ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2")
        ]
        cursor.executemany("""
            INSERT INTO products (user_id, name, description, category, image_url, regular_price, discount_price, deal_expiry, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, products)

        conn.commit()


if __name__ == "__main__":
    seed_data()
    print("Seed data inserted successfully!")
