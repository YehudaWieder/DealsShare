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
def create_product(user_email, name, description, category, image_url, regular_price, discount_price, deal_expiry, link):
    """Insert a new product into the database."""
    query = """
        INSERT INTO products
        (user_email, name, description, category, image_url, regular_price, discount_price, deal_expiry, link)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    product_id = run_query(query, (user_email, name, description, category, image_url, regular_price, discount_price, deal_expiry, link), return_lastrowid=True)
    return product_id

def get_product(product_id):
    """Retrieve a single product by ID."""
    query = """
        SELECT user_email, id, name, description, category, image_url, regular_price, discount_price, deal_expiry, link
        FROM products WHERE id = ?
    """
    result = run_query(query, (product_id,), fetch=True)
    if result:
        row = result[0]
        return {
            "user_email": row[0], 
            "id": row[1], 
            "name": row[2], 
            "description": row[3], 
            "category": row[4],
            "image_url": row[5], 
            "regular_price": row[6], 
            "discount_price": row[7],
            "deal_expiry": row[8], 
            "product_link": row[9]
        }
    return None

def get_products(offset=0, limit=PRODUCTS_PER_PAGE):
    """Retrieve a range of products with all fields."""
    query = """
        SELECT user_email, id, name, description, category, image_url,
               regular_price, discount_price, deal_expiry, link
        FROM products
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (limit, offset), fetch=True)
    return [
        {
            "user_email": row[0], 
            "id": row[1], 
            "name": row[2], 
            "description": row[3], 
            "category": row[4],
            "image_url": row[5], 
            "regular_price": row[6], 
            "discount_price": row[7],
            "deal_expiry": row[8], 
            "product_link": row[9]
        }
        for row in result
    ]

def get_user_products(user_email, offset=0, limit=PRODUCTS_PER_PAGE):
    """Retrieve a range of products for a specific user."""
    query = """
        SELECT user_email, id, name, description, category, image_url,
               regular_price, discount_price, deal_expiry, link
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
            "description": row[3], 
            "category": row[4],
            "image_url": row[5], 
            "regular_price": row[6], 
            "discount_price": row[7],
            "deal_expiry": row[8], 
            "product_link": row[9]
        }
        for row in result
    ]
    
def get_user_favorites(user_email):
    """
    Retrieve all products liked by a specific user.
    Returns a list of product rows.
    """
    query = """
        SELECT p.*
        FROM products p
        JOIN favorites f ON p.id = f.product_id
        WHERE f.user_email = ?
    """
    return run_query(query, (user_email,), fetch=True)


def update_product(product_id, name=None, description=None, category=None,
                   image_url=None, regular_price=None, discount_price=None,
                   deal_expiry=None, link=None):
    """
    Update product fields by ID. Only provided fields will be updated.
    """
    fields = []
    params = []

    if name is not None:
        fields.append("name = ?")
        params.append(name)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if image_url is not None:
        fields.append("image_url = ?")
        params.append(image_url)
    if regular_price is not None:
        fields.append("regular_price = ?")
        params.append(regular_price)
    if discount_price is not None:
        fields.append("discount_price = ?")
        params.append(discount_price)
    if deal_expiry is not None:
        fields.append("deal_expiry = ?")
        params.append(deal_expiry)
    if link is not None:
        fields.append("link = ?")
        params.append(link)

    if not fields:
        return False  # Nothing to update

    params.append(product_id)
    query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
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
