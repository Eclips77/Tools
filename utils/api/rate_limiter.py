
from typing import Dict
import time
from collections import defaultdict

class RateLimiter:
    """Simple token-bucket style in-memory rate limiter per key."""

    def __init__(self, rate: float, capacity: int) -> None:
        """
        Args:
            rate: Tokens added per second.
            capacity: Bucket capacity.
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens: Dict[str, float] = defaultdict(lambda: float(capacity))
        self.timestamps: Dict[str, float] = defaultdict(lambda: time.time())

    def _refill(self, key: str) -> None:
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.timestamps[key]
        self.tokens[key] = min(self.capacity, self.tokens[key] + elapsed * self.rate)
        self.timestamps[key] = now

    def allow(self, key: str, cost: float = 1.0) -> bool:
        """Check if an action is allowed; consume tokens if possible."""
        self._refill(key)
        if self.tokens[key] >= cost:
            self.tokens[key] -= cost
            return True
        return False

def main() -> None:
    rl = RateLimiter(rate=5, capacity=10)
    print([rl.allow("ip1") for _ in range(12)])

if __name__ == "__main__":
    main()
