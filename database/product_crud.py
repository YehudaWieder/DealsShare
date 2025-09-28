from datetime import datetime
from typing import Optional, Dict, List, Union, Set
import sqlite3

from config import DB_PATH, PRODUCTS_PER_PAGE
from database.user_crud import get_seller_avg_rating, get_user

# -------------------------
# Utility function
# -------------------------
def run_query(query: str, params: tuple = (), fetch: bool = False, return_lastrowid: bool = False) -> Optional[Union[List[tuple], int]]:
    """
    Execute a SQL query with optional fetch or return last inserted row ID.
    """
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

# -------------------------
# CRUD Functions
# -------------------------
def create_product(
    seller_email: str, name: str, features: str, free_shipping: bool, description: str,
    category: str, regular_price: float, discount_price: float, image_url: str, link: str,
    publish_date: datetime
) -> int:
    """
    Insert a new product into the database.
    """
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

def update_product(
    product_id: int, name: Optional[str] = None, features: Optional[str] = None,
    free_shipping: Optional[bool] = None, description: Optional[str] = None,
    category: Optional[str] = None, regular_price: Optional[float] = None,
    discount_price: Optional[float] = None, image_url: Optional[str] = None,
    link: Optional[str] = None, publish_date: Optional[datetime] = None
) -> bool:
    """
    Update specified fields of a product by ID.
    Only provided fields will be updated.
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
        return False

    query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
    params.append(product_id)
    run_query(query, tuple(params))
    return True

def delete_old_products() -> None:
    """Delete products older than 10 days."""
    query = """
        DELETE FROM products
        WHERE julianday('now') - julianday(publish_date) > 10
    """
    run_query(query)

def delete_product(product_id: int) -> bool:
    """Delete a product by ID."""
    query = "DELETE FROM products WHERE id = ?"
    run_query(query, (product_id,))
    return True

# -------------------------
# Fetch Products
# -------------------------
def get_user_favorite_ids(user_email: str) -> Set[int]:
    """Return set of product IDs favorited by user."""
    rows = run_query(
        "SELECT product_id FROM favorites WHERE user_email = ?",
        (user_email,), fetch=True
    )
    return {row[0] for row in rows}

def get_product_avg_rating(product_id: int) -> float:
    """Return average rating of a product."""
    query = "SELECT AVG(rating) FROM ratings WHERE product_id = ?"
    result = run_query(query, (product_id,), fetch=True)
    return round(result[0][0], 1) if result and result[0][0] is not None else 0.0

def get_product(product_id: int, user_email: Optional[str] = None, include_seller_info: bool = True) -> Optional[dict]:
    """
    Fetch single product by ID.
    Includes seller info and favorite status if requested.
    """
    products = get_products(product_id=product_id, offset=0, limit=1)

    if not products:
        return None

    product = products[0]

    if user_email:
        favorite_ids = get_user_favorite_ids(user_email)
        product['is_favorite'] = product['id'] in favorite_ids

    if include_seller_info:
        seller = get_user(product['seller_email'])
        product['seller_name'] = f"{seller['first_name']} {seller['last_name']}"
        product['seller_rating'] = get_seller_avg_rating(product['seller_email'])

    return product

def get_products(
    product_id: Optional[int] = None,
    category_name: Optional[str] = None,
    seller_email: Optional[str] = None,
    user_email: Optional[str] = None,
    offset: int = 0,
    limit: int = PRODUCTS_PER_PAGE,
    filters: Optional[Dict] = None,
    include_seller_info: bool = True,
    include_product_rating: bool = True,
    include_favorites: bool = True,
    only_favorites: bool = False
) -> List[dict]:
    """
    Fetch products list with dynamic filters.
    """
    filters = filters or {}
    where_clauses = []
    params = []

    from_clause = "FROM products p"

    if product_id:
        where_clauses.append("p.id = ?")
        params.append(product_id)

    if only_favorites and user_email:
        from_clause += " JOIN favorites f ON p.id = f.product_id"
        where_clauses.append("f.user_email = ?")
        params.append(user_email)

    if category_name:
        where_clauses.append("LOWER(p.category) = LOWER(?)")
        params.append(category_name)

    if seller_email:
        where_clauses.append("p.seller_email = ?")
        params.append(seller_email)

    if filters.get("free_shipping"):
        where_clauses.append("p.free_shipping = 1")

    if search_query := filters.get("search_query"):
        where_clauses.append("p.name LIKE ?")
        params.append(f"%{search_query}%")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT p.seller_email, p.id, p.name, p.features, p.free_shipping,
               p.description, p.category, p.regular_price, p.discount_price,
               p.image_url, p.link, p.publish_date
        {from_clause}
        WHERE {where_sql}
        LIMIT ? OFFSET ?
    """
    rows = run_query(query, tuple(params + [limit, offset]), fetch=True)

    favorite_ids = []
    if include_favorites and user_email and not only_favorites:
        favorite_ids = get_user_favorite_ids(user_email)

    products = []
    for row in rows:
        prod = {
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
            "publish_date": datetime.strptime(row[11], "%Y-%m-%d %H:%M:%S")
        }

        if include_seller_info:
            seller = get_user(prod["seller_email"])
            prod["seller_name"] = f"{seller['first_name']} {seller['last_name']}"
            prod["seller_rating"] = get_seller_avg_rating(seller["email"])

        if include_product_rating:
            prod["product_rating"] = get_product_avg_rating(prod["id"])

        if include_favorites:
            prod["is_favorite"] = True if only_favorites else (prod["id"] in favorite_ids)

        products.append(prod)

    return products

def count_products(
    category_name: Optional[str] = None,
    seller_email: Optional[str] = None,
    user_email: Optional[str] = None,
    filters: Optional[Dict] = None
) -> int:
    """
    Count products in the database with flexible filters.
    """
    filters = filters or {}
    where_clauses = []
    params = []

    from_clause = "FROM products p"
    if user_email:
        from_clause += " JOIN favorites f ON p.id = f.product_id"
        where_clauses.append("f.user_email = ?")
        params.append(user_email)

    if category_name:
        where_clauses.append("LOWER(p.category) = LOWER(?)")
        params.append(category_name)

    if seller_email:
        where_clauses.append("p.seller_email = ?")
        params.append(seller_email)

    if filters.get("free_shipping"):
        where_clauses.append("p.free_shipping = 1")

    if search_query := filters.get("search_query"):
        where_clauses.append("p.name LIKE ?")
        params.append(f"%{search_query}%")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    query = f"""
        SELECT COUNT(*)
        {from_clause}
        WHERE {where_sql}
    """
    return run_query(query, tuple(params), fetch=True)[0][0]

# -------------------------
# Ratings and Favorites
# -------------------------
def rate_product(user_email: str, product_id: int, rating: int) -> bool:
    """
    Add or update a user's rating for a product.
    Each user can rate a product only once.
    """
    product = run_query(
        "SELECT seller_email FROM products WHERE id = ?",
        (product_id,), fetch=True
    )

    if not product or product[0][0] == user_email:
        return False

    seller_email = product[0][0]

    existing = run_query(
        "SELECT id FROM ratings WHERE user_email = ? AND product_id = ?",
        (user_email, product_id), fetch=True
    )

    if existing:
        run_query(
            "UPDATE ratings SET rating = ? WHERE id = ?",
            (rating, existing[0][0])
        )
    else:
        run_query(
            "INSERT INTO ratings (user_email, seller_email, product_id, rating) VALUES (?, ?, ?, ?)",
            (user_email, seller_email, product_id, rating)
        )
    return True

def toggle_favorite(user_email: str, product_id: int) -> bool:
    """
    Add or remove a product from user's favorites.
    Returns True if added, False if removed.
    """
    product = run_query(
        "SELECT id FROM products WHERE id = ?",
        (product_id,), fetch=True
    )
    if not product:
        return None

    existing = run_query(
        "SELECT 1 FROM favorites WHERE user_email = ? AND product_id = ?",
        (user_email, product_id), fetch=True
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
