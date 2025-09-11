import os

# Flask settings
secret_key = "2cf31a1bd8ebdf07f9e94bc2332b1df4"

# Database settings
DB_PATH = "database/deals.db"

# JWT settings

# File upload settings
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

# Other settings
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
