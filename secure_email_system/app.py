from flask import Flask, render_template, session, redirect, url_for
from config import Config
from database.db import mysql
from routes.auth_routes import auth
from routes.email_routes import email_bp


# ==========================
# Create Flask App
# ==========================
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize MySQL
mysql.init_app(app)

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(email_bp)


# ==========================
# Home Route
# ==========================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================
# Dashboard Route
# ==========================
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    username = user[0]

    return render_template("dashboard.html", username=username)


# ==========================
# Logout Route
# ==========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ==========================
# Run App
# ==========================
if __name__ == "__main__":
    app.run(debug=True)