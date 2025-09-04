
from typing import Any, List, Optional
from queue import Queue, Empty

class QueueManager:
    """Thread-safe FIFO queue utilities with helpful extras."""

    def __init__(self, maxsize: int = 0) -> None:
        self.q: Queue = Queue(maxsize=maxsize)

    def enqueue(self, item: Any) -> None:
        """Put an item into the queue."""
        self.q.put(item)

    def enqueue_bulk(self, items: List[Any]) -> None:
        """Put multiple items into the queue."""
        for i in items:
            self.q.put(i)

    def dequeue(self, timeout: Optional[float] = None) -> Any:
        """Get an item, optionally with timeout."""
        try:
            return self.q.get(timeout=timeout)
        except Empty:
            return None

    def size(self) -> int:
        """Current queue size."""
        return self.q.qsize()

    def is_empty(self) -> bool:
        """Whether the queue is empty."""
        return self.q.empty()

    def clear(self) -> None:
        """Clear the queue."""
        while not self.q.empty():
            try:
                self.q.get_nowait()
            except Empty:
                break

def main() -> None:
    qm = QueueManager()
    qm.enqueue_bulk([1,2,3])
    print(qm.size())
    print(qm.dequeue())

if __name__ == "__main__":
    main()
