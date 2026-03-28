from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64


# ==========================
# Generate 256-bit AES Key
# ==========================
def generate_aes_key():
    return get_random_bytes(32)  # 32 bytes = 256 bits


# ==========================
# Encrypt Message Using AES (EAX Mode)
# ==========================
def encrypt_message(aes_key, message):

    if isinstance(message, str):
        message = message.encode()

    cipher = AES.new(aes_key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(message)

    # Combine nonce + tag + ciphertext
    encrypted_data = cipher.nonce + tag + ciphertext

    return base64.b64encode(encrypted_data).decode()


# ==========================
# Decrypt Message Using AES
# ==========================
def decrypt_message(aes_key, encrypted_data):

    try:
        raw = base64.b64decode(encrypted_data)

        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]

        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)

        decrypted_message = cipher.decrypt_and_verify(ciphertext, tag)

        return decrypted_message.decode()

    except Exception:
        # If tampered or invalid
        return None