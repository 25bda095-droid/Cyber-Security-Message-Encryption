from src.constants import AES_TYPE, RSA_TYPE, RSA_MAX_BYTES
from src.crypto.aes_crypto import AESCrypto
from src.crypto.rsa_crypto import RSACrypto
from src.utils.encoding import bytes_to_base64, base64_to_bytes


def encrypt_message(message, encryption_type):
    if encryption_type == AES_TYPE:
        key = AESCrypto.generate_key()
        encrypted_message, iv = AESCrypto.encrypt(message, key)

        return {
            "encrypted_message": encrypted_message,
            "encryption_key": bytes_to_base64(key),
            "iv": iv,
            "public_key": "",
            "encryption_type_used": AES_TYPE
        }

    if encryption_type == RSA_TYPE:
        msg_size = len(message) if isinstance(message, bytes) else len(message.encode("utf-8"))

        if msg_size > RSA_MAX_BYTES:
            raise ValueError("Message too large for RSA encryption. Use AES-256 for larger messages.")

        public_key, private_key = RSACrypto.generate_keys()
        encrypted_message = RSACrypto.encrypt(message, public_key)

        return {
            "encrypted_message": encrypted_message,
            "encryption_key": private_key,
            "iv": "",
            "public_key": public_key,
            "encryption_type_used": RSA_TYPE
        }


def decrypt_message(encrypted_message, key_input, encryption_type, iv_input=None):
    if encryption_type == AES_TYPE:
        key = base64_to_bytes(key_input)
        return AESCrypto.decrypt(encrypted_message, key, iv_input)

    if encryption_type == RSA_TYPE:
        return RSACrypto.decrypt(encrypted_message, key_input)