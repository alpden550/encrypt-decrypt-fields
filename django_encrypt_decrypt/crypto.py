import base64
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Crypto:
    def __init__(self, key: str):
        self.key = key

    def get_key(self) -> bytes:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(self.key.encode())
        return base64.urlsafe_b64encode(digest.finalize())

    def encrypt(self, password: str) -> str:
        fernet = Fernet(self.get_key())
        return fernet.encrypt(password.encode()).decode()

    def decrypt_token(self, token: Optional[str]) -> Optional[str]:
        if token is None:
            return

        fernet = Fernet(self.get_key())
        return fernet.decrypt(token.encode()).decode()
