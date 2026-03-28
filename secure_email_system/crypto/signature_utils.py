from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
import base64
import os


# ==========================
# Sign Message using RSA Private Key
# ==========================
def sign_message(private_path, message):

    try:
        if not os.path.exists(private_path):
            return None

        # Convert message safely
        if isinstance(message, str):
            message = message.encode()

        with open(private_path, "rb") as f:
            private_key = RSA.import_key(f.read())

        hash_obj = SHA512.new(message)

        signature = pkcs1_15.new(private_key).sign(hash_obj)

        return base64.b64encode(signature).decode()

    except Exception:
        return None


# ==========================
# Verify Digital Signature
# ==========================
def verify_signature(public_key_str, message, signature):

    try:
        if isinstance(message, str):
            message = message.encode()

        public_key = RSA.import_key(public_key_str)

        hash_obj = SHA512.new(message)

        decoded_signature = base64.b64decode(signature)

        pkcs1_15.new(public_key).verify(hash_obj, decoded_signature)

        return True

    except Exception:
        return False