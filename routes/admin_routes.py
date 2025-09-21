

from math import ceil
from config import USERS_PER_PAGE
from database.product_crud import count_user_products
from database.user_crud import count_users, delete_user, get_all_users, get_seller_avg_rating, get_user, update_user

def get_all_users_with_stats(offset: int, limit: int, filters: dict = None) -> list:
    """
    Retrieve all users along with their product statistics.
    """
    users = get_all_users(offset=offset, limit=limit, filters=filters)

    for user in users:
        user["product_count"] = count_user_products(user["email"])
        user["avg_rating"] = get_seller_avg_rating(user["email"])
        
    return users

def edit_user_details(form_data) -> dict:
    """
    Main function to update an existing user from form data.
    Returns a dictionary with success status and message.
    """
    user_email = form_data.get("email")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    role = form_data.get("role")
    
    # Check if the user exists in DB
    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    # Update user in DB
    try:
        update_user(user_email, first_name=first_name, last_name=last_name, password=existing_user["password"], role=role)
        return {"success": True, "message": "User updated successfully."}
    except Exception as e:
        print(e)
        return {"success": False, "message": f"Error while updating user: {str(e)}"}
    

def delete_user_by_id(form_data) -> dict:
    """
    Main function to delete an existing user by ID.
    Returns a dictionary with success status and message.
    """
    user_email = form_data.get("user_email")
    
    # Check if the user exists in DB
    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    # Delete user from DB
    try:
        delete_user(user_email)
        return {"success": True, "message": "User deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting user: {str(e)}"}


def is_user_admin(user_id: int) -> dict:
    """
    Check if a given user is an admin.
    Returns a dictionary with success status, message.
    """

    # Fetch user from DB
    existing_user = get_user(user_id)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    try:
        # Check if the user's role is ADMIN
        if existing_user.get("role", "").upper() == "ADMIN":
            return {"success": True, "message": "User is an admin."}
        else:
            return {"success": False, "message": "User is not an admin."}

    except Exception as e:
        return {"success": False, "message": f"Error while checking admin status: {str(e)}"}

def calculate_users_pagination_data(page: int, filters: dict = None) -> list:
    """
    Calculate pagination data for users.
    """
    offset = (page - 1) * USERS_PER_PAGE
    total_count = count_users(filters=filters)
    total_pages = ceil(total_count / USERS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }