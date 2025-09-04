
from typing import Any, Dict
import time
import bcrypt
import jwt

class AuthManager:
    """JWT-based auth utilities and password hashing helpers."""

    def __init__(self, secret: str, algo: str = "HS256", default_exp: int = 3600) -> None:
        self.secret = secret
        self.algo = algo
        self.default_exp = default_exp

    def hash_password(self, password: str) -> bytes:
        """Hash a plaintext password using bcrypt."""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def verify_password(self, password: str, hashed: bytes) -> bool:
        """Verify a password against a bcrypt hash."""
        return bcrypt.checkpw(password.encode("utf-8"), hashed)

    def create_token(self, subject: str, expires_in: int = None, **claims: Any) -> str:
        """Create a signed JWT for a subject with optional extra claims."""
        now = int(time.time())
        payload: Dict[str, Any] = {"sub": subject, "iat": now, "exp": now + (expires_in or self.default_exp)}
        payload.update(claims)
        return jwt.encode(payload, self.secret, algorithm=self.algo)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode and validate a JWT, returning the payload."""
        return jwt.decode(token, self.secret, algorithms=[self.algo])

def main() -> None:
    am = AuthManager("secret")
    h = am.hash_password("pass")
    print("Verify:", am.verify_password("pass", h))
    t = am.create_token("user123", role="admin")
    print("Token:", t)
    print("Payload:", am.decode_token(t))

if __name__ == "__main__":
    main()
