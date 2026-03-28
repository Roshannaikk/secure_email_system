from flask import Blueprint, request, session, render_template, redirect, url_for
from database.db import mysql
from crypto.rsa_utils import generate_keys
import bcrypt

auth = Blueprint("auth", __name__)


# ==========================
# REGISTER ROUTE
# ==========================
@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        return render_template("register.html", error="All fields are required")

    cur = mysql.connection.cursor()

    # Check if username or email already exists
    cur.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
    existing_user = cur.fetchone()

    if existing_user:
        cur.close()
        return render_template("register.html", error="Username or Email already exists")

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        # Insert into users table
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s,%s,%s)",
            (username, email, hashed_password.decode())
        )

        user_id = cur.lastrowid

        # Generate RSA keys
        public_key, private_path = generate_keys(username)

        # Store key information
        cur.execute(
            "INSERT INTO user_keys (user_id, public_key, private_key_path) VALUES (%s,%s,%s)",
            (user_id, public_key, private_path)
        )

        mysql.connection.commit()

    except Exception as e:
        mysql.connection.rollback()
        cur.close()
        return render_template("register.html", error="Registration failed")

    cur.close()

    return render_template("register.html", message="User Registered Successfully. Please Login.")


# ==========================
# LOGIN ROUTE
# ==========================
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("login.html", error="All fields are required")

    cur = mysql.connection.cursor()

    cur.execute("SELECT id, password_hash FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    if not user:
        cur.close()
        return render_template("login.html", error="Invalid Credentials")

    user_id = user[0]
    stored_password = user[1]

    # Check password
    if bcrypt.checkpw(password.encode(), stored_password.encode()):

        session["user_id"] = user_id

        # Log login activity
        cur.execute(
            "INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)",
            (user_id, "SUCCESS")
        )

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("dashboard"))

    else:
        # Log failed login attempt
        cur.execute(
            "INSERT INTO login_activity (user_id, login_status) VALUES (%s, %s)",
            (user_id, "FAILED")
        )

        mysql.connection.commit()
        cur.close()

        return render_template("login.html", error="Invalid Credentials")