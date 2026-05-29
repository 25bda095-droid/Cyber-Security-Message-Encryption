from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from src.utils.encoding import bytes_to_base64, base64_to_bytes


class RSACrypto:
    @staticmethod
    def generate_keys():
        key = RSA.generate(2048)

        private_key = key.export_key().decode("utf-8")
        public_key = key.publickey().export_key().decode("utf-8")

        return public_key, private_key

    @staticmethod
    def encrypt(message, public_key_pem):
        if isinstance(message, str):
            message = message.encode("utf-8")

        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)

        ciphertext = cipher.encrypt(message)

        return bytes_to_base64(ciphertext)

    @staticmethod
    def decrypt(encrypted_message, private_key_pem):
        ciphertext = base64_to_bytes(encrypted_message)

        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)

        decrypted = cipher.decrypt(ciphertext)

        return decrypted.decode("utf-8")