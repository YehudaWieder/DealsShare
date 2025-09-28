import bcrypt
from typing import Dict

from config import USERS_PER_PAGE
from database.user_crud import delete_user, get_user, get_seller_avg_rating, update_user
from database.product_crud import count_products


def get_user_with_stats(email: str) -> dict:
    """
    Retrieve user details along with their product statistics.
    Returns a dict with user info or error message if not found.
    """
    user = get_user(email)
    if not user:
        return {"success": False, "message": "User not found."}

    # Add product count and average rating
    user["product_count"] = count_products(seller_email=email)
    user["avg_rating"] = get_seller_avg_rating(email)

    return user


def edit_profile_details(form_data: dict) -> Dict:
    """
    Update an existing user's profile using form data.
    Returns a dict with success status and message.
    """
    email = form_data.get("user_id")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    new_email = form_data.get("email")
    current_password = form_data.get("current_password")
    new_password = form_data.get("new_password")

    # Fetch user and verify password
    existing_user = get_user(email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    if not bcrypt.checkpw(current_password.encode(), existing_user["password"]):
        return {"success": False, "message": "Incorrect password. Please try again."}

    # Hash new password if provided, else keep current password
    if new_password:
        password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    else:
        password_hash = bcrypt.hashpw(current_password.encode(), bcrypt.gensalt())

    # Update user in DB
    try:
        update_user(
            email,
            first_name=first_name,
            last_name=last_name,
            new_email=new_email,
            password=password_hash,
            role=existing_user["role"]
        )
        return {"success": True, "message": "Profile updated successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while updating profile: {str(e)}"}


def delete_profile(form_data: dict) -> Dict:
    """
    Delete a user profile and all related products.
    Returns a dict with success status and message.
    """
    user_email = form_data.get("email")

    # Check if the user exists
    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    # Delete user from DB
    try:
        delete_user(user_email)
        return {"success": True, "message": "User and all products deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting user: {str(e)}"}
