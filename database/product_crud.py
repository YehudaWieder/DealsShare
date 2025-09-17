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
def create_product(seller_email, name, features, free_shipping, description,
                   category, regular_price, discount_price, image_url, link, publish_date):
    """Insert a new product into the database."""
    query = """
        INSERT INTO products
        (seller_email, name, features, free_shipping, description, category, 
         regular_price, discount_price, image_url, link, publish_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    product_id = run_query(query, (
        seller_email, name, features, int(free_shipping), description, category,
        regular_price, discount_price, image_url, link, publish_date
    ), return_lastrowid=True)
    return product_id


def get_product(product_id):
    """Retrieve a single product by ID."""
    query = """
        SELECT seller_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products WHERE id = ?
    """
    result = run_query(query, (product_id,), fetch=True)
    if result:
        row = result[0]
        return {
            "seller_email": row[0],
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
        SELECT seller_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (limit, offset), fetch=True)
    return [
        {
            "seller_email": row[0],
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
    
def get_products_by_category(category_name, offset=0, limit=PRODUCTS_PER_PAGE):
    """
    Retrieve a range of products filtered by category.
    """
    query = """
        SELECT seller_email, id, name, features, free_shipping, description, 
            category, regular_price, discount_price, image_url, link, publish_date
        FROM products
        WHERE LOWER(category) = LOWER(?)
        LIMIT ? OFFSET ?
        """
    result = run_query(query, (category_name, limit, offset), fetch=True)

    return [
        {
            "seller_email": row[0],
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


def get_user_products(seller_email, offset=0, limit=PRODUCTS_PER_PAGE):
    """Retrieve a range of products for a specific user."""
    query = """
        SELECT seller_email, id, name, features, free_shipping, description, 
               category, regular_price, discount_price, image_url, link, publish_date
        FROM products
        WHERE seller_email = ?
        LIMIT ? OFFSET ?
    """
    result = run_query(query, (seller_email, limit, offset), fetch=True)
    return [
        {
            "seller_email": row[0],
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
        SELECT p.seller_email, p.id, p.name, p.features, p.free_shipping, 
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
            "seller_email": row[0],
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

def get_user_favorite_ids(user_email: str) -> set:
    """
    Return a set of product IDs that this user has marked as favorites.
    """
    rows = run_query(
        "SELECT product_id FROM favorites WHERE user_email = ?",
        (user_email,),
        fetch=True
    )
    return {row[0] for row in rows}

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

def count_products_by_category(category_name):
    """
    Return the total number of products in the database for a specific category.
    """
    query = "SELECT COUNT(*) FROM products WHERE LOWER(category) = LOWER(?)"
    result = run_query(query, (category_name,), fetch=True)
    return result[0][0] if result else 0

def count_user_products(seller_email):
    """Return the total number of products for a specific user."""
    query = "SELECT COUNT(*) FROM products WHERE seller_email = ?"
    return run_query(query, (seller_email,), fetch=True)[0][0]

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
    Each user can rate a product only once.
    Rating should be an integer between 1 and 5.
    """
    # Get the seller email from the product
    product = run_query(
        "SELECT seller_email FROM products WHERE id = ?",
        (product_id,),
        fetch=True
    )
    
    seller_email = product[0][0]

    if not product or seller_email == user_email:
        return False  # product not found or user is the seller

    # Check if this user has already rated this product
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
            """
            INSERT INTO ratings (user_email, seller_email, product_id, rating)
            VALUES (?, ?, ?, ?)
            """,
            (user_email, seller_email, product_id, rating)
        )

    return True


def get_product_avg_rating(product_id):
    """
    Get the average rating of a specific product by its ID.
    """
    query = "SELECT AVG(rating) FROM ratings WHERE product_id = ?"
    result = run_query(query, (product_id,), fetch=True)
    return round(result[0][0], 1) if result and result[0][0] is not None else 0.0

def toggle_favorite(user_email, product_id):
    """
    Add or remove a product from user's favorites.
    If the product is already favorited by the user, remove it.
    Otherwise, add it.
    Returns True if added, False if removed.
    """

    product = run_query(
        "SELECT id FROM products WHERE id = ?",
        (product_id,),
        fetch=True
    )

    if not product:
        return None

    existing = run_query(
        "SELECT 1 FROM favorites WHERE user_email = ? AND product_id = ?",
        (user_email, product_id),
        fetch=True
    )

    if existing:
        run_query(
            "DELETE FROM favorites WHERE user_email = ? AND product_id = ?",
            (user_email, product_id)
        )
        return False
    else:
        run_query(
            "INSERT INTO favorites (user_email, product_id) VALUES (?, ?)",
            (user_email, product_id)
        )
        return True
