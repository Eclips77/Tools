
from typing import Dict
import time

class MetricsCollector:
    """In-memory metrics (counters and timers) with simple export."""

    def __init__(self) -> None:
        self.counters: Dict[str, int] = {}
        self.timers: Dict[str, float] = {}

    def inc(self, key: str, value: int = 1) -> None:
        """Increment a counter by value."""
        self.counters[key] = self.counters.get(key, 0) + value

    def start_timer(self, key: str) -> None:
        """Start a timer for a key."""
        self.timers[key] = time.time()

    def stop_timer(self, key: str) -> float:
        """Stop a timer and return elapsed seconds."""
        start = self.timers.pop(key, None)
        if start is None:
            return 0.0
        return time.time() - start

    def export(self) -> Dict[str, Dict]:
        """Export current metrics as a dict."""
        return {"counters": dict(self.counters), "running_timers": list(self.timers.keys())}

def main() -> None:
    m = MetricsCollector()
    m.inc("processed", 3)
    m.start_timer("t1")
    time.sleep(0.01)
    print("Elapsed:", m.stop_timer("t1"))
    print("Export:", m.export())

if __name__ == "__main__":
    main()
