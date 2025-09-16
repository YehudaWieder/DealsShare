from datetime import datetime
import sqlite3

from config import DB_PATH, PRODUCTS_PER_PAGE

# --- Utility ---
def run_query(query, params=(), fetch=False, return_lastrowid=False):
    """Execute a SQL query with optional parameters and optional fetch."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        if fetch:
            return cursor.fetchall()
        if return_lastrowid:
            return cursor.lastrowid
        return None

# --- CRUD Functions ---
def create_product(user_email, name, features, free_shipping, description,
                   category, regular_price, discount_price, image_url, link, publish_date):
    """Insert a new product into the database."""
    query = """
        INSERT INTO products
        (user_email, name, features, free_shipping, description, category, 
         regular_price, discount_price, image_url, link, publish_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    product_id = run_query(query, (
        user_email, name, features, int(free_shipping), description, category,
        regular_price, discount_price, image_url, link, publish_date
    ), return_lastrowid=True)
    return product_id


def get_product(product_id):
    """Retrieve a single product by ID."""
    query = """
        SELECT user_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products WHERE id = ?
    """
    result = run_query(query, (product_id,), fetch=True)
    if result:
        row = result[0]
        return {
            "user_email": row[0],
            "id": row[1],
            "name": row[2],
            "features": row[3],
            "free_shipping": bool(row[4]),
            "description": row[5],
            "category": row[6],
            "regular_price": row[7],
            "discount_price": row[8],
            "image_url": row[9],
            "product_link": row[10],
            "publish_date": datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S.%f")
        }
    return None


def get_all_products(offset=0, limit=PRODUCTS_PER_PAGE):
    """Retrieve a range of products with all fields."""
    query = """
        SELECT user_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (limit, offset), fetch=True)
    return [
        {
            "user_email": row[0],
            "id": row[1],
            "name": row[2],
            "features": row[3],
            "free_shipping": bool(row[4]),
            "description": row[5],
            "category": row[6],
            "regular_price": row[7],
            "discount_price": row[8],
            "image_url": row[9],
            "product_link": row[10],
            "publish_date": datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S.%f")
        }
        for row in result
    ]


def get_user_products(user_email, offset=0, limit=PRODUCTS_PER_PAGE):
    """Retrieve a range of products for a specific user."""
    query = """
        SELECT user_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products
        WHERE user_email = ?
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (user_email, limit, offset), fetch=True)
    return [
        {
            "user_email": row[0],
            "id": row[1],
            "name": row[2],
            "features": row[3],
            "free_shipping": bool(row[4]),
            "description": row[5],
            "category": row[6],
            "regular_price": row[7],
            "discount_price": row[8],
            "image_url": row[9],
            "product_link": row[10],
            "publish_date": datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S.%f")
        }
        for row in result
    ]


def get_user_favorites(user_email, offset=0, limit=PRODUCTS_PER_PAGE):
    """
    Retrieve all products liked by a specific user.
    Returns a list of product dicts.
    """
    query = """
        SELECT p.user_email, p.id, p.name, p.features, p.free_shipping, 
               p.description, p.category, p.regular_price, p.discount_price, 
               p.image_url, p.link, p.publish_date
        FROM products p
        JOIN favorites f ON p.id = f.product_id
        WHERE f.user_email = ?
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (user_email, limit, offset), fetch=True)
    return [
        {
            "user_email": row[0],
            "id": row[1],
            "name": row[2],
            "features": row[3],
            "free_shipping": bool(row[4]),
            "description": row[5],
            "category": row[6],
            "regular_price": row[7],
            "discount_price": row[8],
            "image_url": row[9],
            "product_link": row[10],
            "publish_date": datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S.%f")
        }
        for row in result
    ]


def update_product(product_id, name=None, features=None, free_shipping=None, description=None,
                   category=None, regular_price=None, discount_price=None,
                   image_url=None, link=None, publish_date=None):
    """
    Update product fields by ID. Only provided fields will be updated.
    """
    fields = []
    params = []

    if name is not None:
        fields.append("name = ?")
        params.append(name)
    if features is not None:
        fields.append("features = ?")
        params.append(features)
    if free_shipping is not None:
        fields.append("free_shipping = ?")
        params.append(int(free_shipping))
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if regular_price is not None:
        fields.append("regular_price = ?")
        params.append(regular_price)
    if discount_price is not None:
        fields.append("discount_price = ?")
        params.append(discount_price)
    if image_url is not None:
        fields.append("image_url = ?")
        params.append(image_url)
    if link is not None:
        fields.append("link = ?")
        params.append(link)
    if publish_date is not None:
        fields.append("publish_date = ?")
        params.append(publish_date)

    if not fields:
        return False  # Nothing to update

    query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
    params.append(product_id)
    run_query(query, tuple(params))
    return True

def delete_product(product_id):
    """Delete a product by ID."""
    query = "DELETE FROM products WHERE id = ?"
    run_query(query, (product_id,))
    return True

def count_products():
    """Return the total number of products in the database."""
    query = "SELECT COUNT(*) FROM products"
    return run_query(query, fetch=True)[0][0]

def count_user_products(user_email):
    """Return the total number of products for a specific user."""
    query = "SELECT COUNT(*) FROM products WHERE user_email = ?"
    return run_query(query, (user_email,), fetch=True)[0][0]

def count_user_favorites(user_email):
    """
    Count the number of products liked by a specific user.
    """
    query = "SELECT COUNT(*) FROM favorites WHERE user_email = ?"
    result = run_query(query, (user_email,), fetch=True)
    return result[0][0] if result else 0

def rate_product(user_email, product_id, rating):
    """
    Add or update a user's rating for a product.
    Rating should be an integer between 1 and 5.
    """
    # Check if the user has already rated the product
    existing = run_query(
        "SELECT id FROM ratings WHERE user_email = ? AND product_id = ?",
        (user_email, product_id),
        fetch=True
    )
    if existing:
        # Update existing rating
        run_query(
            "UPDATE ratings SET rating = ? WHERE id = ?",
            (rating, existing[0][0])
        )
    else:
        # Insert new rating
        run_query(
            "INSERT INTO ratings (user_email, product_id, rating) VALUES (?, ?, ?)",
            (user_email, product_id, rating)
        )
    return True