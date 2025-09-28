import bcrypt
from typing import Dict

from database.user_crud import create_user, get_user


def is_user_exist(email: str) -> bool | dict:
    """
    Check if a user with the given email exists in the database.
    Returns the user dict if exists, otherwise False.
    """
    user = get_user(email)
    return user if user else False


def insert_new_user(form_data: dict) -> Dict:
    """
    Insert a new user from form data.
    Returns a dict with success status and message.
    """
    email = form_data.get("email")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    gender = form_data.get("gender")
    raw_password = form_data.get("password")
    role = form_data.get("role", "user")  # default role

    # Hash password
    password = bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt())

    # Check if user already exists
    if is_user_exist(email):
        return {"success": False, "message": "User with this email already exists."}

    # Insert new user into DB
    create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        password=password,
        role=role
    )

    return {"success": True, "message": "User registered successfully."}


def user_login(form_data: dict) -> Dict:
    """
    Validate user login.
    - Checks if the email exists.
    - Checks if the password matches the hashed password in DB.
    Returns a dict with success status and message.
    """
    email = form_data.get("email")
    password = form_data.get("password")

    # Fetch user
    user = is_user_exist(email)
    if not user:
        return {"success": False, "message": "User with this email does not exist."}

    # Verify password
    if bcrypt.checkpw(password.encode(), user["password"]):
        return {"success": True, "message": "Login successful.", "email": user["email"]}
    else:
        return {"success": False, "message": "Incorrect password."}
