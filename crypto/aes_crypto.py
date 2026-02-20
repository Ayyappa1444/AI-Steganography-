from cryptography.fernet import Fernet
import hashlib
import base64

def _derive_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )

def encrypt_text(plain_text: str, password: str) -> str:
    fernet = Fernet(_derive_key(password))
    return fernet.encrypt(plain_text.encode()).decode()

def decrypt_text(cipher_text: str, password: str) -> str:
    fernet = Fernet(_derive_key(password))
    return fernet.decrypt(cipher_text.encode()).decode()
