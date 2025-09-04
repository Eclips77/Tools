
from typing import Callable, Dict, List, Any, DefaultDict
from collections import defaultdict

class EventBus:
    """In-memory Pub/Sub event bus."""

    def __init__(self) -> None:
        self.subscribers: DefaultDict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        """Subscribe a handler to a topic."""
        self.subscribers[topic].append(handler)

    def unsubscribe(self, topic: str, handler: Callable[[Any], None]) -> None:
        """Unsubscribe a handler from a topic."""
        self.subscribers[topic] = [h for h in self.subscribers[topic] if h is not handler]

    def publish(self, topic: str, message: Any) -> None:
        """Publish a message to all subscribers of a topic."""
        for handler in self.subscribers[topic]:
            handler(message)

    def topics(self) -> List[str]:
        """List available topics with subscribers."""
        return [t for t, hs in self.subscribers.items() if hs]

def main() -> None:
    bus = EventBus()
    bus.subscribe("news", lambda m: print("news:", m))
    bus.publish("news", {"title": "Hello"})
    print("Topics:", bus.topics())

if __name__ == "__main__":
    main()
