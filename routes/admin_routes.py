from math import ceil
from typing import List, Dict, Optional

from config import USERS_PER_PAGE
from database.product_crud import count_products
from database.user_crud import (
    count_users,
    delete_user,
    get_all_users,
    get_seller_avg_rating,
    get_user,
    update_user
)


def get_all_users_with_stats(offset: int, limit: int, filters: Optional[dict] = None) -> List[Dict]:
    """
    Retrieve all users along with their product statistics:
    - product_count: total products by the user
    - avg_rating: average rating of user's products
    """
    users = get_all_users(offset=offset, limit=limit, filters=filters)

    for user in users:
        user["product_count"] = count_products(seller_email=user["email"])
        user["avg_rating"] = get_seller_avg_rating(user["email"])

    return users


def edit_user_details(form_data: dict) -> Dict:
    """
    Update an existing user from form data.
    Returns a dict with success status and message.
    """
    user_email = form_data.get("email")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    role = form_data.get("role")

    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    try:
        update_user(
            user_email,
            first_name=first_name,
            last_name=last_name,
            password=existing_user["password"],
            role=role
        )
        return {"success": True, "message": "User updated successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while updating user: {str(e)}"}


def delete_user_by_id(form_data: dict) -> Dict:
    """
    Delete an existing user by email.
    Returns a dict with success status and message.
    """
    user_email = form_data.get("user_email")

    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    try:
        delete_user(user_email)
        return {"success": True, "message": "User deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting user: {str(e)}"}


def is_user_admin(user_email: str) -> Dict:
    """
    Check if a given user is an admin.
    Returns a dict with success status and message.
    """
    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    try:
        if existing_user.get("role", "").upper() == "ADMIN":
            return {"success": True, "message": "User is an admin."}
        else:
            return {"success": False, "message": "User is not an admin."}
    except Exception as e:
        return {"success": False, "message": f"Error while checking admin status: {str(e)}"}


def calculate_users_pagination_data(page: int, filters: Optional[dict] = None) -> Dict:
    """
    Calculate pagination data for users.
    Returns dict with page, offset, and total_pages.
    """
    offset = (page - 1) * USERS_PER_PAGE
    total_count = count_users(filters=filters)
    total_pages = ceil(total_count / USERS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }
