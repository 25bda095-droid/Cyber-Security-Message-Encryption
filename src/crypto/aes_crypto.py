from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

from src.utils.encoding import bytes_to_base64, base64_to_bytes


class AESCrypto:
    @staticmethod
    def generate_key():
        return get_random_bytes(32)

    @staticmethod
    def encrypt(message, key):
        cipher = AES.new(key, AES.MODE_CBC)

        if isinstance(message, str):
            message = message.encode("utf-8")

        padded_message = pad(message, AES.block_size)
        ciphertext = cipher.encrypt(padded_message)

        encrypted_message = bytes_to_base64(ciphertext)
        iv = bytes_to_base64(cipher.iv)

        return encrypted_message, iv

    @staticmethod
    def decrypt(encrypted_message, key, iv):
        ciphertext = base64_to_bytes(encrypted_message)
        iv_bytes = base64_to_bytes(iv)

        cipher = AES.new(key, AES.MODE_CBC, iv_bytes)

        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size)

        return decrypted.decode("utf-8")