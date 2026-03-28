import os


class Config:

    # ==========================
    # Flask Secret Key
    # ==========================
    SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_key_change_this")

    # ==========================
    # MySQL Configuration
    # ==========================
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root"
    MYSQL_DB = "secure_email_system"

    # Required for flask-mysqldb
    MYSQL_CURSORCLASS = "Cursor"

    # ==========================
    # Key Storage Folder
    # ==========================
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    KEY_FOLDER = os.path.join(BASE_DIR, "keys", "user_keys")