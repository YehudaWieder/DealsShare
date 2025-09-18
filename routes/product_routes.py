from datetime import datetime
from math import ceil
import os
from PIL import Image
from werkzeug.utils import secure_filename
import config
from database.product_crud import count_products, count_products_by_category, count_user_favorites, count_user_products, create_product, delete_product, get_all_products, get_product, get_product_avg_rating, get_products_by_category, get_user_favorite_ids, get_user_favorites, get_user_products, update_product
from database.user_crud import get_user, get_seller_avg_rating

UPLOAD_FOLDER = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
PRODUCTS_PER_PAGE = config.PRODUCTS_PER_PAGE

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_resize_image(file, product_id, max_size=(800, 800)):
    """
    Save the uploaded image to the uploads folder and resize it.
    Returns the relative path to be stored in the DB.
    """
    if not file:
        return "/img/default.png"
    
    if not allowed_file(file.filename):
        return None

    # Extract the extension and ensure it's lowercase
    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return None

    # Generate a safe filename and deleting the previous file if exist
    filename = f"product_{product_id}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    try:
        # Open image and resize
        image = Image.open(file)
        image.thumbnail(max_size)  # Resize while maintaining aspect ratio
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

        # Determine correct PIL format
        if ext in ['jpg', 'jpeg']:
            image_format = 'JPEG'
        elif ext == 'png':
            image_format = 'PNG'
        elif ext == 'gif':
            image_format = 'GIF'
        else:
            image_format = None  # fallback if unknown
        if image_format is None:
            return None

        image.save(filepath, format=image_format)
        return f"uploads/{filename}"

    except Exception as e:
        print("Error saving image:", e)
        return None

def insert_new_product(form_data, file, user_email) -> dict:
    """
    Main function to insert a new product from form data and uploaded image.
    Returns a dictionary with success status and message.
    """
    name = form_data.get("name")
    features = form_data.get("features")  # string like: "עמיד למים, קל משקל"
    free_shipping = form_data.get("free_shipping", "0")  # checkbox: "on" or None
    description = form_data.get("description")
    category = form_data.get("category")
    regular_price = form_data.get("regular_price")
    discount_price = form_data.get("discount_price")
    link = form_data.get("link")
    publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize free_shipping
    free_shipping = 1 if free_shipping in ("1", "true", "True", "on") else 0

    ext = file.filename.rsplit(".", 1)[1].lower()

    # Insert product into DB (use a temp image_url initially)
    product_id = create_product(
        seller_email=user_email,
        name=name,
        features=features,
        free_shipping=free_shipping,
        description=description,
        category=category,
        regular_price=regular_price,
        discount_price=discount_price,
        image_url=f"temp_name.{ext}",
        link=link,
        publish_date=publish_date
    )

    # Handle image saving
    image_url = save_and_resize_image(file, product_id)
    if not image_url:
        delete_product(product_id)
        return {"success": False, "message": "Invalid image."}

    update_product(product_id, image_url=image_url)

    return {"success": True, "message": "Product added successfully.", "product_id": product_id}


def update_product_in_db(form_data, file) -> dict:
    """
    Main function to update an existing product from form data.
    Returns a dictionary with success status and message.
    """
    product_id = form_data.get("product_id")
    name = form_data.get("name", None)
    features = form_data.get("features", None)
    free_shipping = form_data.get("free_shipping", None)
    description = form_data.get("description", None)
    category = form_data.get("category", None)
    regular_price = form_data.get("regular_price", None)
    discount_price = form_data.get("discount_price", None)
    link = form_data.get("link", None)
    publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize free_shipping if provided
    if free_shipping is not None:
        free_shipping = 1 if free_shipping in ("1", "true", "True", "on") else 0

    # Check if the product exists in DB
    existing_product = get_product(product_id)
    if not existing_product:
        return {"success": False, "message": "Product not found."}

    # Handle image upload
    try:
        img = Image.open(file)
        img.verify()
        image_url = save_and_resize_image(file, product_id=product_id)
    except:
        image_url = existing_product['image_url']
    if not image_url:
        return {"success": False, "message": "Invalid image."}

    try:
        update_product(
            product_id=product_id,
            name=name,
            features=features,
            free_shipping=free_shipping,
            description=description,
            category=category,
            image_url=image_url,
            regular_price=regular_price,
            discount_price=discount_price,
            link=link,
            publish_date=publish_date
        )
        return {"success": True, "message": "Product updated successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while updating product: {str(e)}"}


def delete_product_by_id(form_data) -> dict:
    """
    Main function to delete an existing product by ID.
    Returns a dictionary with success status and message.
    """
    product_id = form_data.get("product_id")

    # Check if the product exists in DB
    existing_product = get_product(product_id)
    if not existing_product:
        return {"success": False, "message": "Product not found."}

    # Delete product from DB
    try:
        delete_product(product_id)

        file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(existing_product['image_url']))
        if os.path.exists(file_path) and "example.png" not in file_path and "image1.jpg" not in file_path and "image2.jpg" not in file_path:
            os.remove(file_path)
            
        return {"success": True, "message": "Product deleted successfully."}
    except Exception as e:
        print({"success": False, "message": f"Error while deleting product: {str(e)}"})
        return {"success": False, "message": f"Error while deleting product: {str(e)}"}

def get_all_products_with_seller_info(user_email: str, offset: int, limit: int, filters: dict = None) -> list:
    """
    Fetch products with seller info, ratings, and favorites, applying optional filters.
    """
    filters = filters or {}
    products = get_all_products(offset=offset, limit=limit, filters=filters)
    favorite_ids = get_user_favorite_ids(user_email) if user_email else []

    for product in products:
        seller = get_user(product['seller_email'])
        product['seller_name'] = f"{seller['first_name']} {seller['last_name']}"
        product['seller_rating'] = get_seller_avg_rating(seller['email'])
        product['product_rating'] = get_product_avg_rating(product['id'])
        product['is_favorite'] = product['id'] in favorite_ids

    return products



def get_products_by_category_with_seller_info(category_name: str, user_email: str, offset: int, limit: int, filters: dict = None) -> list:
    """
    Fetch products by category along with their seller info and whether they are favorited by this user.
    """
    filters = filters or {}
    products = get_products_by_category(category_name, offset=offset, limit=limit, filters=filters)
    favorite_ids = get_user_favorite_ids(user_email)

    for product in products:
        seller = get_user(product['seller_email'])
        product['seller_name'] = seller['first_name'] + ' ' + seller['last_name']
        product['seller_rating'] = get_seller_avg_rating(seller['email'])
        product['is_favorite'] = product['id'] in favorite_ids

    return products

def get_user_products_with_ratings(user_email: str, offset, limit, filters: dict = None) -> list:
    """
    Fetch all products of a specific user and include each product's average rating.
    """
    products = get_user_products(seller_email=user_email, offset=offset, limit=limit, filters=filters)

    for product in products:
        product['product_rating'] = get_product_avg_rating(product['id'])

    return products


def get_all_favorite_products_with_seller_info(user_email: str, offset: int, limit: int, filters: dict = None) -> list:
    """
    Fetch all favorite products of a user along with their seller info from the database.
    Returns a list of favorite products with seller details.
    """
    products = get_user_favorites(user_email=user_email, offset=offset, limit=limit, filters=filters)
    
    for product in products:
        seller = get_user(product['seller_email'])
        product['seller_name'] = seller['first_name'] + ' ' + seller['last_name']  
        product['seller_rating'] = get_seller_avg_rating(product['seller_email'])
        product['is_favorite'] = True
        
    return products

def get_product_with_seller_info(user_email, product_id: int) -> dict:
    """
    Fetch a single product along with its seller info from the database by product ID.
    Returns a dictionary with product and seller details.
    """
    product = get_product(product_id)
    favorite_ids = get_user_favorite_ids(user_email)


    seller = get_user(product['seller_email'])
    product['seller_name'] = seller['first_name'] + ' ' + seller['last_name']
    product['seller_email'] = seller['email']
    product['seller_rating'] = get_seller_avg_rating(product['seller_email'])
    product['is_favorite'] = product['id'] in favorite_ids
    
    return product

def calculate_pagination_data(page: int, filters: dict = None) -> dict:
    """
    Calculate pagination data based on the current page and optional filters.
    Returns a dictionary containing the current page, offset, and total pages.
    """
    offset = (page - 1) * PRODUCTS_PER_PAGE
    total_count = count_products(filters=filters)
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }

    
def calculate_pagination_data_by_category(category_name: str, page: int, filters: dict = None) -> dict:
    """
    Calculate pagination data for products filtered by category.
    """
    offset = (page - 1) * PRODUCTS_PER_PAGE
    total_count = count_products_by_category(category_name, filters=filters)
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }

def calculate_pagination_data_favorites(user_email: str, page: int, filters: dict = None) -> dict:
    """
    Calculate pagination data for the user's favorite products.
    """
    offset = (page - 1) * PRODUCTS_PER_PAGE
    total_count = count_user_favorites(user_email, filters=filters)
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }

def calculate_pagination_data_by_user(user_email: str, page: int, filters: dict = None) -> dict:
    """
    Calculate pagination data for products posted by a specific user.
    """
    offset = (page - 1) * PRODUCTS_PER_PAGE
    total_count = count_user_products(user_email, filters=filters)
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE)

    return {
        "page": page,
        "offset": offset,
        "total_pages": total_pages
    }
