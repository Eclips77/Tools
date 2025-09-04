
import time
from typing import Any, Dict, Optional, Tuple

class CacheManager:
    """Simple in-memory TTL cache with get/set/delete and auto-expiry."""

    def __init__(self) -> None:
        self.store: Dict[str, Tuple[Any, Optional[float]]] = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value with optional TTL in seconds."""
        exp = time.time() + ttl if ttl else None
        self.store[key] = (value, exp)

    def get(self, key: str) -> Optional[Any]:
        """Get a value if not expired; otherwise return None."""
        val = self.store.get(key)
        if not val:
            return None
        value, exp = val
        if exp and exp < time.time():
            del self.store[key]
            return None
        return value

    def delete(self, key: str) -> None:
        """Delete a key if present."""
        self.store.pop(key, None)

    def clear(self) -> None:
        """Clear the entire cache."""
        self.store.clear()

def main() -> None:
    c = CacheManager()
    c.set("k", "v", ttl=1)
    print(c.get("k"))

if __name__ == "__main__":
    main()
