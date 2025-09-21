import sqlite3

from config import DB_PATH, USERS_PER_PAGE

# --- Utility ---
def run_query(query, params=(), fetch=False):
    """
    Execute a SQL query with optional parameters and optional fetch.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        
        if fetch:
            return cursor.fetchall()
        return None

# --- CRUD Functions ---
def create_user(email, first_name, last_name, gender, password, role):
    """
    Insert a new user into the database.
    """
    query = """
        INSERT INTO users (email, first_name, last_name, gender, password, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    run_query(query, (email, first_name, last_name, gender, password, role))
    return True


def get_user(email):
    """
    Retrieve a single user by email.
    """
    query = """
        SELECT email, first_name, last_name, gender, password, role
        FROM users
        WHERE email = ?
    """
    result = run_query(query, (email,), fetch=True)
    if result:
        row = result[0]
        return {
            "email": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "gender": row[3],
            "password": row[4],
            "role": row[5],
        }
    return None


def get_all_users(offset=0, limit=USERS_PER_PAGE, filters: dict = None):
    """
    Retrieve all users (without password).
    """
    filters = filters or {}
    where_clauses = ["1=1"]
    params = []

    # Filter: search query
    if search_query := filters.get("search_query"):
        where_clauses.append("(first_name LIKE ? OR last_name LIKE ?)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])
  
    where_sql = " AND ".join(where_clauses)
    
    query = f"""
        SELECT email, first_name, last_name, gender, role
        FROM users
        WHERE {where_sql}
        LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])
    
    result = run_query(query, params, fetch=True)
    return [
        {
        "email": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "gender": row[3],
        "role": row[4],
        }
        for row in result
    ]


def update_user(email, new_email=None, first_name=None,
                last_name=None, gender=None, password=None, role=None):
    """
    Update user fields by email. Only provided fields will be updated.
    """
    fields = []
    params = []


    if new_email:
        fields.append("email = ?")
        params.append(new_email)
    if first_name:
        fields.append("first_name = ?")
        params.append(first_name)
    if last_name:
        fields.append("last_name = ?")
        params.append(last_name)
    if gender:
        fields.append("gender = ?")
        params.append(gender)
    if password:
        fields.append("password = ?")
        params.append(password)
    if role:
        fields.append("role = ?")
        params.append(role)

    if not fields:
        return False  # Nothing to update

    params.append(email)
    query = f"UPDATE users SET {', '.join(fields)} WHERE email = ?"
    run_query(query, tuple(params))
    return True


def delete_user(email):
    """
    Delete a user by email.
    """
    query = "DELETE FROM users WHERE email = ?"
    run_query(query, (email,))
    return True


def count_users(filters: dict = None):
    """
    Count the number of users in the database.
    """
    filters = filters or {}
    where_clauses = ["1=1"]
    params = []

    # Filter: search query
    if search_query := filters.get("search_query"):
        where_clauses.append("(first_name LIKE ? OR last_name LIKE ?)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    
    where_sql = " AND ".join(where_clauses)
    
    query = f"SELECT COUNT(*) FROM users WHERE {where_sql}"
    return run_query(query, params, fetch=True)[0][0]


def get_seller_avg_rating(seller_email):
    """
    Get the average rating of all products created by a specific seller.
    """
    query = "SELECT AVG(rating) FROM ratings WHERE seller_email = ?"
    result = run_query(query, (seller_email,), fetch=True)
    return round(result[0][0], 1) if result and result[0][0] is not None else 0.0

