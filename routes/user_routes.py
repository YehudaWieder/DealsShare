

from math import ceil
import bcrypt
from config import USERS_PER_PAGE
from database.user_crud import count_users, delete_user, get_all_users, get_user, get_seller_avg_rating, update_user
from database.product_crud import count_user_favorites, count_user_products

def get_user_with_stats(email):
    """
    Retrieve user details along with their product statistics.
    """
    user = get_user(email)
    if not user:
        return {"success": False, "message": "User not found."}

    user["product_count"] = count_user_products(email)
    user["avg_rating"] = get_seller_avg_rating(email)

    return user

def get_all_users_with_stats():
    """
    Retrieve all users along with their product statistics.
    """
    users = get_all_users()

    for user in users:
        user["product_count"] = count_user_products(user["email"])
        user["avg_rating"] = get_seller_avg_rating(user["email"])
        
    return users

def edit_profile_details(form_data) -> dict:
    """
    Main function to update an existing user from form data.
    Returns a dictionary with success status and message.
    """
    email = form_data.get("user_id")
    first_name = form_data.get("first_name")
    last_name = form_data.get("last_name")
    new_email = form_data.get("email")
    password = form_data.get("current_password")
    new_password = form_data.get("new_password")

        
    # Check if the user exists in DB and if the password is correct
    existing_user = get_user(email)
    if not existing_user:
        return {"success": False, "message": "User not found."}
    
    if not bcrypt.checkpw(password.encode(), existing_user["password"]):
        return {"success": False, "message": "Incorrect password please try again."}

    if new_password != "":
        password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    else:
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Update user in DB
    try:
        update_user(email, first_name=first_name, last_name=last_name, new_email=new_email, password=password, role=existing_user["role"])
        return {"success": True, "message": "Profile updated successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while updating profile: {str(e)}"}
    
    
def delete_profile(form_data) -> dict:
    """
    Main function to delete an existing user by ID.
    Returns a dictionary with success status and message.
    """
    user_id = form_data.get("email")
    
    # Check if the user exists in DB
    existing_user = get_user(user_id)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    # Delete user from DB
    try:
        delete_user(user_id)
        return {"success": True, "message": "User with his all products deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting user: {str(e)}"}
    
def calculate_users_pagination_data(page: int) -> dict:
    """
    Calculate pagination data for users.
    """
    offset = (page - 1) * USERS_PER_PAGE
    total_count = count_users()
    total_pages = ceil(total_count / USERS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }