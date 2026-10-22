import hashlib
import base64
class Crypto:
    @staticmethod
    def hash_master(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    @staticmethod
    def derive_key(password: str) -> bytes:
        return hashlib.sha256(password.encode()).digest()
    @staticmethod
    def encrypt(text: str, password: str) -> str:
        key = Crypto.derive_key(password)
        text_bytes = text.encode()
        encrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(text_bytes)])
        return base64.b64encode(encrypted).decode()
    @staticmethod
    def decrypt(enc_text: str, password: str) -> str:
        key = Crypto.derive_key(password)
        enc_bytes = base64.b64decode(enc_text.encode())
        decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(enc_bytes)])
        return decrypted.decode()
