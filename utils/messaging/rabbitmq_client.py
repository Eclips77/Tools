
from typing import Callable, Optional
import pika

class RabbitMQClient:
    """Generic RabbitMQ producer/consumer using pika."""

    def __init__(self, url: str = "amqp://guest:guest@localhost:5672/") -> None:
        self.params = pika.URLParameters(url)

    def publish(self, queue: str, body: str) -> None:
        """Publish a message to a queue (auto-declare)."""
        conn = pika.BlockingConnection(self.params)
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=True)
        ch.basic_publish(exchange="", routing_key=queue, body=body.encode("utf-8"), properties=pika.BasicProperties(delivery_mode=2))
        conn.close()

    def consume(self, queue: str, handler: Callable[[str], None], auto_ack: bool = False) -> None:
        """Consume messages from a queue and pass body to handler."""
        conn = pika.BlockingConnection(self.params)
        ch = conn.channel()
        ch.queue_declare(queue=queue, durable=True)

        def _cb(ch_, method, properties, body):
            msg = body.decode("utf-8")
            handler(msg)
            if not auto_ack:
                ch_.basic_ack(delivery_tag=method.delivery_tag)

        ch.basic_qos(prefetch_count=1)
        ch.basic_consume(queue=queue, on_message_callback=_cb, auto_ack=auto_ack)
        try:
            ch.start_consuming()
        finally:
            conn.close()

def main() -> None:
    print("RabbitMQClient ready. Requires RabbitMQ server to publish/consume.")

if __name__ == "__main__":
    main()
