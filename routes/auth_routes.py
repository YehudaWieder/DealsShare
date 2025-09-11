import bcrypt

from database.user_crud import create_user, find_user


def is_user_exist(email: str) -> bool:
    """
    Check if a user with the given email already exists in the database.
    """
    user = find_user(email)
    if user:
        return user
    return False

def insert_new_user(form_data) -> dict:
    """
    Main function to insert a new user from form data.
    Returns a dictionary with success status and message.
    """
    username = form_data.get("username")
    email = form_data.get("email")
    password = bcrypt.hashpw(form_data.get("password").encode(), bcrypt.gensalt())
    role = form_data.get("role", "user")  # default role

    # Check if user already exists
    if is_user_exist(email):
        return {"success": False, "message": "User with this email already exists."}

    # insert new User into DB
    create_user(username=username, email=email, password=password, role=role)

    return {"success": True, "message": "User registered successfully."}


def user_login(form_data) -> dict:
    """
    Validate user login.
    Checks if the email exists and if the password matches the hashed password in DB.
    Returns a dictionary with success status and message.
    """
    email = form_data.get("email")
    password = form_data.get("password")

    # Check if user exists
    user = is_user_exist(email)
    if not user:
        return {"success": False, "message": "User with this email does not exist."}

    # Check password
    if bcrypt.checkpw(password.encode(), user["password"]):
        return {"success": True, "message": "Login successfully.", "user_id": user["user_id"]}
    else:
        return {"success": False, "message": "Incorrect password"}