from flask import Blueprint, request, session, render_template, redirect, url_for
from database.db import mysql
from crypto.aes_utils import generate_aes_key, encrypt_message, decrypt_message
from crypto.rsa_utils import encrypt_with_rsa, decrypt_with_rsa
from crypto.hash_utils import generate_hash
from crypto.signature_utils import sign_message, verify_signature
import base64

email_bp = Blueprint("email", __name__)


# ==========================
# COMPOSE EMAIL PAGE
# ==========================
@email_bp.route("/compose", methods=["GET"])
def compose():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    # Fetch all users except current user
    cur.execute("SELECT id, username FROM users WHERE id != %s", (user_id,))
    users = cur.fetchall()
    cur.close()

    return render_template("compose.html", users=users)


# ==========================
# SEND EMAIL
# ==========================
@email_bp.route("/send", methods=["POST"])
def send_email():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    sender_id = session["user_id"]
    receiver_id = request.form.get("receiver_id")
    message = request.form.get("message")

    if not receiver_id or not message:
        return redirect(url_for("email.compose"))

    cur = mysql.connection.cursor()

    # Get receiver public key
    cur.execute("SELECT public_key FROM user_keys WHERE user_id=%s", (receiver_id,))
    receiver_key_data = cur.fetchone()

    if not receiver_key_data:
        cur.close()
        return redirect(url_for("email.compose"))

    receiver_public_key = receiver_key_data[0]

    # Get sender private key path
    cur.execute("SELECT private_key_path FROM user_keys WHERE user_id=%s", (sender_id,))
    sender_key_data = cur.fetchone()

    if not sender_key_data:
        cur.close()
        return redirect(url_for("email.compose"))

    private_path = sender_key_data[0]

    # ========================
    # Hybrid Encryption Process
    # ========================

    # 1️⃣ Hash message
    message_hash = generate_hash(message)

    # 2️⃣ Sign message
    signature = sign_message(private_path, message)

    # 3️⃣ Generate AES key
    aes_key = generate_aes_key()

    # 4️⃣ Encrypt message with AES
    encrypted_message = encrypt_message(aes_key, message)

    # 5️⃣ Encrypt AES key with receiver RSA
    encrypted_aes_key = encrypt_with_rsa(receiver_public_key, aes_key)
    encrypted_aes_key = base64.b64encode(encrypted_aes_key).decode()

    # ========================
    # Store in Database
    # ========================
    cur.execute("""
        INSERT INTO emails 
        (sender_id, receiver_id, encrypted_message, encrypted_aes_key, digital_signature)
        VALUES (%s,%s,%s,%s,%s)
    """, (sender_id, receiver_id, encrypted_message, encrypted_aes_key, signature))

    email_id = cur.lastrowid

    cur.execute("""
        INSERT INTO email_security_metadata 
        (email_id, message_hash)
        VALUES (%s,%s)
    """, (email_id, message_hash))

    mysql.connection.commit()
    cur.close()

    return redirect(url_for("email.inbox"))


# ==========================
# INBOX LIST PAGE
# ==========================
@email_bp.route("/inbox", methods=["GET"])
def inbox():

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    # Get emails received by user
    cur.execute("""
        SELECT e.id, u.username, e.sent_at
        FROM emails e
        JOIN users u ON e.sender_id = u.id
        WHERE e.receiver_id = %s
        ORDER BY e.sent_at DESC
    """, (user_id,))

    emails = cur.fetchall()
    cur.close()

    return render_template("inbox_list.html", emails=emails)


# ==========================
# READ & VERIFY EMAIL
# ==========================
@email_bp.route("/inbox/<int:email_id>", methods=["GET"])
def read_email(email_id):

    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT e.encrypted_message, e.encrypted_aes_key, e.digital_signature,
               sender_keys.public_key, receiver_keys.private_key_path,
               u.username
        FROM emails e
        JOIN users u ON e.sender_id = u.id
        JOIN user_keys sender_keys ON e.sender_id = sender_keys.user_id
        JOIN user_keys receiver_keys ON e.receiver_id = receiver_keys.user_id
        WHERE e.id=%s AND e.receiver_id=%s
    """, (email_id, user_id))

    data = cur.fetchone()

    if not data:
        cur.close()
        return redirect(url_for("email.inbox"))

    encrypted_message, encrypted_aes_key, signature, sender_public_key, private_path, sender_username = data

    # Decrypt AES key
    encrypted_aes_key = base64.b64decode(encrypted_aes_key)
    aes_key = decrypt_with_rsa(private_path, encrypted_aes_key)

    # Decrypt message
    decrypted_message = decrypt_message(aes_key, encrypted_message)

    # Verify signature
    valid = verify_signature(sender_public_key, decrypted_message, signature)

    cur.close()

    return render_template(
        "read_email.html",
        sender=sender_username,
        message=decrypted_message,
        signature_valid=valid
    )