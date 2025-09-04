
from typing import Any, Dict, Optional
import redis

class RedisClient:
    """Generic Redis client for strings, hashes, and pub/sub operations."""

    def __init__(self, url: str = "redis://localhost:6379/0") -> None:
        self.r = redis.from_url(url, decode_responses=True)

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """Set a key with optional expiration."""
        return bool(self.r.set(key, value, ex=ex))

    def get(self, key: str) -> Optional[str]:
        """Get a key value."""
        return self.r.get(key)

    def delete(self, key: str) -> int:
        """Delete a key."""
        return self.r.delete(key)

    def incr(self, key: str) -> int:
        """Atomically increment a key."""
        return self.r.incr(key)

    def hset(self, name: str, mapping: Dict[str, Any]) -> int:
        """Set multiple hash fields."""
        return self.r.hset(name, mapping=mapping)

    def hgetall(self, name: str) -> Dict[str, str]:
        """Get entire hash."""
        return self.r.hgetall(name)

    def publish(self, channel: str, message: str) -> int:
        """Publish a message to a channel."""
        return self.r.publish(channel, message)

    def subscribe(self, channel: str):
        """Generator yielding messages from a channel."""
        pubsub = self.r.pubsub()
        pubsub.subscribe(channel)
        for msg in pubsub.listen():
            if msg.get("type") == "message":
                yield msg["data"]

def main() -> None:
    client = RedisClient()
    client.set("hello", "world", ex=60)
    print("Get:", client.get("hello"))
    print("Hash:", client.hgetall("meta"))

if __name__ == "__main__":
    main()
