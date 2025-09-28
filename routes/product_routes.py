from datetime import datetime
from math import ceil
import os
from typing import Dict, Optional
from PIL import Image

import config
from database.product_crud import count_products, create_product, delete_product, get_product, update_product

UPLOAD_FOLDER = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
PRODUCTS_PER_PAGE = config.PRODUCTS_PER_PAGE


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_and_resize_image(file, product_id: int, max_size=(800, 800)) -> Optional[str]:
    """
    Save the uploaded image to the uploads folder and resize it.
    Returns the relative path to be stored in the DB, or None if invalid.
    """
    if not file or not allowed_file(file.filename):
        return "/img/default.png"

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"product_{product_id}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Remove old file if exists
    if os.path.exists(filepath):
        os.remove(filepath)

    try:
        image = Image.open(file)
        image.thumbnail(max_size)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Determine PIL format
        image_format = {"jpg": "JPEG", "jpeg": "JPEG", "png": "PNG", "gif": "GIF"}.get(ext)
        if not image_format:
            return None

        image.save(filepath, format=image_format)
        return f"uploads/{filename}"
    except Exception as e:
        print("Error saving image:", e)
        return None


def insert_new_product(form_data: dict, file, user_email: str, publish_date: Optional[str] = None) -> Dict:
    """
    Insert a new product with optional uploaded image.
    Returns a dictionary with success status and message.
    """
    name = form_data.get("name")
    features = form_data.get("features")
    free_shipping = 1 if form_data.get("free_shipping") in ("1", "true", "True", "on") else 0
    description = form_data.get("description")
    category = form_data.get("category")
    regular_price = form_data.get("regular_price")
    discount_price = form_data.get("discount_price")
    link = form_data.get("link")
    publish_date = publish_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ext = file.filename.rsplit(".", 1)[1].lower()

    # Insert product with temporary image_url
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

    # Save actual image
    image_url = save_and_resize_image(file, product_id)
    if not image_url:
        delete_product(product_id)
        return {"success": False, "message": "Invalid image."}

    update_product(product_id, image_url=image_url)
    return {"success": True, "message": "Product added successfully.", "product_id": product_id}


def update_product_in_db(form_data: dict, file=None) -> Dict:
    """
    Update an existing product with form data and optional image file.
    Returns a dictionary with success status and message.
    """
    product_id = form_data.get("product_id")
    existing_product = get_product(product_id)
    if not existing_product:
        return {"success": False, "message": "Product not found."}

    # Extract fields
    name = form_data.get("name")
    features = form_data.get("features")
    free_shipping = form_data.get("free_shipping")
    if free_shipping is not None:
        free_shipping = 1 if free_shipping in ("1", "true", "True", "on") else 0
    description = form_data.get("description")
    category = form_data.get("category")
    regular_price = form_data.get("regular_price")
    discount_price = form_data.get("discount_price")
    link = form_data.get("link")
    publish_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Handle image
    if file:
        try:
            Image.open(file).verify()
            image_url = save_and_resize_image(file, product_id)
            # Remove old image
            old_image_path = os.path.join(UPLOAD_FOLDER, os.path.basename(existing_product['image_url']))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        except:
            image_url = existing_product['image_url']
    else:
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


def delete_product_by_id(form_data: dict) -> Dict:
    """
    Delete a product by ID.
    Returns a dictionary with success status and message.
    """
    product_id = form_data.get("product_id")
    existing_product = get_product(product_id)
    if not existing_product:
        return {"success": False, "message": "Product not found."}

    try:
        delete_product(product_id)
        file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(existing_product['image_url']))
        if os.path.exists(file_path) and "example.png" not in file_path:
            os.remove(file_path)
        return {"success": True, "message": "Product deleted successfully."}
    except Exception as e:
        return {"success": False, "message": f"Error while deleting product: {str(e)}"}


def calculate_pagination_data(
    page: int,
    filters: dict = None,
    category_name: str = None,
    seller_email: str = None,
    user_email: str = None,
    favorites: bool = False
) -> dict:
    """
    Calculate pagination data for products with optional filters.
    """
    filters = filters or {}
    offset = (page - 1) * PRODUCTS_PER_PAGE

    total_count = count_products(
        category_name=category_name,
        seller_email=seller_email if not favorites else None,
        user_email=user_email if favorites else (user_email if seller_email is None else None),
        filters=filters
    )
    total_pages = ceil(total_count / PRODUCTS_PER_PAGE) if total_count else 1

    return {"page": page, "offset": offset, "total_pages": total_pages}
