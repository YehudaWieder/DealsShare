import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.auth_routes import insert_new_user
from routes.product_routes import insert_new_product
from config import DB_PATH

DB_PATH = DB_PATH


def seed_data():
    users = [
    ("user", "admin@admin.com", "123456", "admin"),
    ("user1", "user1@user1.com", "123456", "user"),
    ("user2", "user2@user2.com", "123456", "user"),
    ("user3", "user3@user3.com", "123456", "user"),
    ("user4", "user4@user4.com", "123456", "user"),
    ("user5", "user5@user5.com", "123456", "user"),
    ("user6", "user6@user6.com", "123456", "user")
    ]

    for user in users:
        form_data = {
            "username": user[0],
            "email": user[1],
            "password": user[2],
            "role": user[3]
        }
        result = insert_new_user(form_data)

        # Sample products
    products = [
        ("2", "Product 1", "This is a short sample product description text.", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("3", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("2", "Product 2", "Description 2", "Category 2", "", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("3", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("5", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("6", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("2", "Product 1", "Description 1", "Category 1", "", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("3", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("5", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("6", "Product 1", "Description 1", "Category 1", "/uploads/example.png", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("2", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("6", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("2", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("3", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("2", "Product 2", "Description 2", "Category 2", "", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("3", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("5", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("6", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("2", "Product 1", "Description 1", "Category 1", "", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("3", "Product 2", "Description 2", "Category 2", "/uploads/example.png", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("1", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("5", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("6", "Product 1", "Description 1", "Category 1", "/uploads/example.png", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("1", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2"),
        ("2", "Product 1", "Description 1", "Category 1", "/uploads/image1.jpg", 100.0, 80.0, "2025-09-30", "http://example.com/1"),
        ("6", "Product 2", "Description 2", "Category 2", "/uploads/image2.jpg", 200.0, 150.0, "2025-10-15", "http://example.com/2")
    ]
    
    for p in products:
        user_id = p[0]
        name = p[1]
        description = p[2]
        category = p[3]
        image_path = p[4]
        regular_price = p[5]
        discount_price = p[6]
        deal_expiry = p[7]
        link = p[8]

        form_data = {
            "name": name,
            "description": description,
            "category": category,
            "regular_price": regular_price,
            "discount_price": discount_price,
            "deal_expiry": deal_expiry,
            "link": link
        }

        file = image_path if image_path else None

        result = insert_new_product(form_data, file, user_id)


if __name__ == "__main__":
    seed_data()
    print("Seed data inserted successfully!")
