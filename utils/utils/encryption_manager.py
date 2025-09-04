
from typing import Optional
from cryptography.fernet import Fernet

class EncryptionManager:
    """Symmetric encryption utilities using Fernet (AES-128 in CBC + HMAC)."""

    def __init__(self, key: Optional[bytes] = None) -> None:
        self.key = key or Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def encrypt_str(self, text: str) -> bytes:
        """Encrypt a UTF-8 string and return bytes token."""
        return self.fernet.encrypt(text.encode("utf-8"))

    def decrypt_str(self, token: bytes) -> str:
        """Decrypt a token and return UTF-8 string."""
        return self.fernet.decrypt(token).decode("utf-8")

    @staticmethod
    def generate_key() -> bytes:
        """Generate a new Fernet key."""
        return Fernet.generate_key()

def main() -> None:
    em = EncryptionManager()
    t = em.encrypt_str("hello")
    print("Decrypted:", em.decrypt_str(t))

if __name__ == "__main__":
    main()
