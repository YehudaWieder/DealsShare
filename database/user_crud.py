import sqlite3
from typing import List, Dict, Optional

from config import DB_PATH, USERS_PER_PAGE

# -------------------------
# Utility function
# -------------------------
def run_query(query: str, params: tuple = (), fetch: bool = False) -> Optional[list]:
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


# -------------------------
# CRUD Functions
# -------------------------
def create_user(email: str, first_name: str, last_name: str,
                gender: str, password: str, role: str) -> bool:
    """
    Insert a new user into the database.
    """
    query = """
        INSERT INTO users (email, first_name, last_name, gender, password, role)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    run_query(query, (email, first_name, last_name, gender, password, role))
    return True


def get_user(email: str) -> Optional[Dict]:
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


def get_all_users(offset: int = 0, limit: int = USERS_PER_PAGE,
                  filters: Optional[dict] = None) -> List[Dict]:
    """
    Retrieve all users (without passwords) with optional search filter.
    """
    filters = filters or {}
    where_clauses = ["1=1"]
    params = []

    # Search filter
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

    result = run_query(query, tuple(params), fetch=True)
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


def update_user(email: str, new_email: Optional[str] = None,
                first_name: Optional[str] = None, last_name: Optional[str] = None,
                gender: Optional[str] = None, password: Optional[str] = None,
                role: Optional[str] = None) -> bool:
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


def delete_user(email: str) -> bool:
    """
    Delete a user by email.
    """
    query = "DELETE FROM users WHERE email = ?"
    run_query(query, (email,))
    return True


def count_users(filters: Optional[dict] = None) -> int:
    """
    Count the number of users in the database with optional search filter.
    """
    filters = filters or {}
    where_clauses = ["1=1"]
    params = []

    # Search filter
    if search_query := filters.get("search_query"):
        where_clauses.append("(first_name LIKE ? OR last_name LIKE ?)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    where_sql = " AND ".join(where_clauses)
    query = f"SELECT COUNT(*) FROM users WHERE {where_sql}"

    return run_query(query, tuple(params), fetch=True)[0][0]


def get_seller_avg_rating(seller_email: str) -> float:
    """
    Get the average rating of all products created by a specific seller.
    """
    query = "SELECT AVG(rating) FROM ratings WHERE seller_email = ?"
    result = run_query(query, (seller_email,), fetch=True)
    return round(result[0][0], 1) if result and result[0][0] is not None else 0.0
