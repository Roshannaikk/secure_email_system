from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


# ==========================
# Generate RSA Key Pair
# ==========================
def generate_keys(username):

    try:
        # Ensure key directory exists
        key_folder = "keys/user_keys"
        os.makedirs(key_folder, exist_ok=True)

        # Generate 2048-bit RSA key
        key = RSA.generate(2048)

        private_key = key.export_key()
        public_key = key.publickey().export_key()

        private_path = os.path.join(key_folder, f"{username}_private.pem")

        # Save private key to file
        with open(private_path, "wb") as f:
            f.write(private_key)

        return public_key.decode(), private_path

    except Exception:
        return None, None


# ==========================
# Encrypt Data with RSA Public Key
# ==========================
def encrypt_with_rsa(public_key_str, data):

    try:
        if isinstance(data, str):
            data = data.encode()

        public_key = RSA.import_key(public_key_str)
        cipher = PKCS1_OAEP.new(public_key)

        encrypted_data = cipher.encrypt(data)

        return encrypted_data

    except Exception:
        return None


# ==========================
# Decrypt Data with RSA Private Key
# ==========================
def decrypt_with_rsa(private_path, encrypted_data):

    try:
        if not os.path.exists(private_path):
            return None

        with open(private_path, "rb") as f:
            private_key = RSA.import_key(f.read())

        cipher = PKCS1_OAEP.new(private_key)

        decrypted_data = cipher.decrypt(encrypted_data)

        return decrypted_data

    except Exception:
        return None