import sqlite3

from config import DB_PATH

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
def create_user(username, email, password, role):
    """
    Insert a new user into the database.
    """
    query = "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)"
    run_query(query, (username, email, password, role))
    return True

def find_user(email):
    """
    Find a user by email and return password.
    """
    query = "SELECT id, username, email, password, role FROM users WHERE email = ?"
    result = run_query(query, (email,), fetch=True)
    if result:
        row = result[0]
        return {
            "user_id": row[0],
            "username": row[1],
            "email": row[2],
            "password": row[3],
            "role": row[4]
        }
    return None

def get_user(user_id):
    """
    Retrieve a single user by ID.
    """
    query = "SELECT id, username, email, password, role FROM users WHERE id = ?"
    result = run_query(query, (user_id,), fetch=True)
    if result:
        row = result[0]
        return {
            "user_id": row[0],
            "username": row[1],
            "email": row[2],
            "password": row[3],
            "role": row[4]
        }
    return None

def get_all_users():
    """
    Retrieve all users.
    """
    query = "SELECT id, username, email, role FROM users"
    result = run_query(query, fetch=True)
    return [
        {"user_id": row[0], "username": row[1], "email": row[2], "role": row[3]}
        for row in result
    ]

def update_user(user_id, username=None, email=None, password=None, role=None):
    """
    Update user fields by ID. Only provided fields will be updated.
    """
    fields = []
    params = []

    if username:
        fields.append("username = ?")
        params.append(username)
    if email:
        fields.append("email = ?")
        params.append(email)
    if password:
        fields.append("password = ?")
        params.append(password)
    if role:
        fields.append("role = ?")
        params.append(role)

    if not fields:
        return False  # Nothing to update

    params.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
    run_query(query, tuple(params))
    return True

def delete_user(user_id):
    """
    Delete a user by ID.
    """
    query = "DELETE FROM users WHERE id = ?"
    run_query(query, (user_id,))
    return True

def count_users():
    """
    Count the number of users in the database.
    """
    query = "SELECT COUNT(*) FROM users"
    return run_query(query, fetch=True)[0][0]

