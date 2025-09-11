import os
from PIL import Image
from werkzeug.utils import secure_filename
from datetime import datetime
import config
from database.product_crud import create_product

# Folder to save uploaded images
UPLOAD_FOLDER = config.UPLOAD_FOLDER
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_and_resize_image(file, max_size=(800, 800)):
    """
    Save the uploaded image to the uploads folder and resize it.
    Returns the relative path to be stored in the DB.
    """
    if not file:
        return "/uploads/example.png"
    
    if not allowed_file(file.filename):
        return None

    # Extract the extension and ensure it's lowercase
    ext = file.filename.rsplit(".", 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return None

    # Generate a safe filename using timestamp and extension
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

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
        return f"/uploads/{filename}"

    except Exception as e:
        print("Error saving image:", e)
        return None

def insert_new_product(form_data, file, user_id) -> dict:
    """
    Main function to insert a new product from form data and uploaded image.
    Returns a dictionary with success status and message.
    """
    name = form_data.get("name")
    description = form_data.get("description")
    category = form_data.get("category")
    regular_price = form_data.get("regular_price")
    discount_price = form_data.get("discount_price")
    deal_expiry = form_data.get("deal_expiry")  # string format: "DD/MM/YYYY"
    link = form_data.get("link")

    # Handle image upload
    image_url = save_and_resize_image(file)
    if not image_url:
        return {"success": False, "message": "Invalid image."}

    # Insert product into DB
    product_id = create_product(
        user_id=user_id,
        name=name,
        description=description,
        category=category,
        image_url=image_url,
        regular_price=regular_price,
        discount_price=discount_price,
        deal_expiry=deal_expiry,
        link=link
    )

    return {"success": True, "message": "Product added successfully.", "product_id": product_id}
