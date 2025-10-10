from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class SymmetricEncryption:
    """Handles AES-256 symmetric encryption and decryption"""
    
    @staticmethod
    def generate_key():
        """Generate a random 256-bit (32 bytes) key"""
        return get_random_bytes(32)
    
    @staticmethod
    def encrypt(message, key):
        """
        Encrypt message using AES-256 in CBC mode
        Returns: (encrypted_message, iv) both base64 encoded
        """
        cipher = AES.new(key, AES.MODE_CBC)
        
        # Convert message to bytes if it's a string
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # Pad message to be multiple of 16 bytes
        padded_message = pad(message, AES.block_size)
        
        # Encrypt
        ciphertext = cipher.encrypt(padded_message)
        
        # Return base64 encoded ciphertext and IV
        return base64.b64encode(ciphertext).decode('utf-8'), \
               base64.b64encode(cipher.iv).decode('utf-8')
    
    @staticmethod
    def decrypt(encrypted_message, key, iv):
        """
        Decrypt message using AES-256
        """
        # Decode from base64
        ciphertext = base64.b64decode(encrypted_message)
        iv_bytes = base64.b64decode(iv)
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
        
        # Decrypt and unpad
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        return decrypted.decode('utf-8')


class AsymmetricEncryption:
    """Handles RSA-2048 asymmetric encryption and decryption"""
    
    @staticmethod
    def generate_keys():
        """
        Generate RSA-2048 key pair
        Returns: (public_key, private_key) as PEM strings
        """
        key = RSA.generate(2048)
        private_key = key.export_key().decode('utf-8')
        public_key = key.publickey().export_key().decode('utf-8')
        return public_key, private_key
    
    @staticmethod
    def encrypt(message, public_key_pem):
        """
        Encrypt message using RSA public key
        Note: RSA can only encrypt small messages (up to 214 bytes for 2048-bit key)
        """
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        # Import public key
        public_key = RSA.import_key(public_key_pem)
        cipher = PKCS1_OAEP.new(public_key)
        
        # Encrypt
        ciphertext = cipher.encrypt(message)
        
        # Return base64 encoded
        return base64.b64encode(ciphertext).decode('utf-8')
    
    @staticmethod
    def decrypt(encrypted_message, private_key_pem):
        """
        Decrypt message using RSA private key
        """
        # Decode from base64
        ciphertext = base64.b64decode(encrypted_message)
        
        # Import private key
        private_key = RSA.import_key(private_key_pem)
        cipher = PKCS1_OAEP.new(private_key)
        
        # Decrypt
        decrypted = cipher.decrypt(ciphertext)
        
        return decrypted.decode('utf-8')


def encrypt_file_content(file_content, encryption_type):
    """
    Encrypt file content based on encryption type
    Returns: encrypted data and keys
    """
    if encryption_type == "Symmetric (AES-256)":
        key = SymmetricEncryption.generate_key()
        encrypted_msg, iv = SymmetricEncryption.encrypt(file_content, key)
        key_str = base64.b64encode(key).decode('utf-8')
        return encrypted_msg, key_str, iv
    else:
        public_key, private_key = AsymmetricEncryption.generate_keys()
        # For large files with RSA, we'd typically use hybrid encryption
        # For this demo, we'll handle small files only
        if len(file_content) > 190:  # RSA limit
            raise ValueError("File too large for RSA encryption. Use symmetric encryption for large files.")
        encrypted_msg = AsymmetricEncryption.encrypt(file_content, public_key)
        return encrypted_msg, public_key, private_key
