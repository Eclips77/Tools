
from typing import Generator, Optional
from kafka import KafkaProducer, KafkaConsumer

class KafkaPubSub:
    """Generic Kafka publisher and subscriber using kafka-python."""

    def __init__(self, bootstrap_servers: str = "localhost:9092", group_id: str = "generic-consumer") -> None:
        self.bootstrap_servers = bootstrap_servers
        self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers, value_serializer=lambda v: str(v).encode("utf-8"))
        self.group_id = group_id

    def publish(self, topic: str, message: str) -> None:
        """Publish a UTF-8 message to a topic."""
        self.producer.send(topic, message)
        self.producer.flush()

    def subscribe(self, topic: str, auto_offset_reset: str = "latest") -> KafkaConsumer:
        """Create a consumer subscribed to a topic."""
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=auto_offset_reset,
            value_deserializer=lambda v: v.decode("utf-8"),
            enable_auto_commit=True,
        )
        return consumer

    def consume_iter(self, topic: str, max_messages: Optional[int] = None) -> Generator[str, None, None]:
        """Yield messages from topic; stop after max_messages if provided."""
        consumer = self.subscribe(topic)
        count = 0
        for record in consumer:
            yield record.value
            count += 1
            if max_messages and count >= max_messages:
                break
        consumer.close()

def main() -> None:
    k = KafkaPubSub()
    print("KafkaPubSub initialized. Use publish/consume_iter with a running Kafka.")

if __name__ == "__main__":
    main()
