import hashlib


# ==========================
# Generate SHA-512 Hash
# ==========================
def generate_hash(message):

    if message is None:
        return None

    # Convert string to bytes safely
    if isinstance(message, str):
        message = message.encode()

    try:
        hash_object = hashlib.sha512(message)
        return hash_object.hexdigest()
    except Exception:
        return None