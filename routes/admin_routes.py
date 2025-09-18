

from database.user_crud import delete_user, get_user, update_user


def edit_user_details(form_data) -> dict:
    """
    Main function to update an existing user from form data.
    Returns a dictionary with success status and message.
    """
    user_email = form_data.get("email")
    username = form_data.get("username")
    role = form_data.get("role")
    
    # Check if the user exists in DB
    existing_user = get_user(user_email)
    if not existing_user:
        return {"success": False, "message": "User not found."}

    # Update user in DB
    try:
        update_user(int(user_email), username=username, email=existing_user["email"], password=existing_user["password"], role=role)
        return {"success": True, "message": "User updated successfully."}
    except Exception as e:
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
