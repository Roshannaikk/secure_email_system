from flask_mysqldb import MySQL

# Create MySQL instance
mysql = MySQL()


def init_db(app):
    """
    Initialize MySQL with Flask app.
    This keeps DB initialization clean and scalable.
    """
    mysql.init_app(app)